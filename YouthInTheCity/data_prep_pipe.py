#These code below are from the "data_prep_pipe.py"
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from termcolor import colored
import mlflow
from memoized_property import memoized_property
from mlflow.tracking import MlflowClient
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.impute import KNNImputer
from sklearn.metrics import r2_score

EXPERIMENT_NAME = "Batch_874_Youth_in_the_city_spatial_regression"
yourname = "Batch_874_Safiaaaaa"
MLFLOW_URI = "https://mlflow.lewagon.ai/"

class Trainer(object):
    def __init__(self, X, y):
        """
            X: pandas DataFrame --> drop the "geometry and the "Kinderarmut"
            y: pandas Series --> "Kinderarmut"
        """
        self.pipeline = None
        self.X = X
        self.y = y
        # for MLFlow
        self.experiment_name = EXPERIMENT_NAME

    def set_experiment_name(self, experiment_name):
        '''defines the experiment name for MLFlow'''
        self.experiment_name = experiment_name

    def set_pipeline(self):
        """defines the pipeline as a class attribute"""
        preproc_pipe = Pipeline([
            ('knnimputer', KNNImputer(missing_values= np.nan)),
            ('robustscaler', RobustScaler())
        ])
        self.pipeline = Pipeline([
            ('preproc', preproc_pipe),
            ('linear_model', LinearRegression())
        ])

    def run(self):
        self.set_pipeline()
        self.mlflow_log_param("model", "Linear")
        self.pipeline.fit(self.X, self.y)

    def evaluate(self, X_test, y_test):
        """evaluates the pipeline on df_test and return the r2 score"""
        y_pred = self.pipeline.predict(X_test)
        score = r2_score(y_test, y_pred)
        self.mlflow_log_metric("r2-score", score)
        return round(score, 2)

    def save_model_locally(self):
        """Save the model into a .joblib format"""
        joblib.dump(self.pipeline, 'model.joblib')
        print(colored("model.joblib saved locally", "green"))

    # MLFlow methods
    @memoized_property
    def mlflow_client(self):
        mlflow.set_tracking_uri(MLFLOW_URI)
        return MlflowClient()

    @memoized_property
    def mlflow_experiment_id(self):
        try:
            return self.mlflow_client.create_experiment(self.experiment_name)
        except BaseException:
            return self.mlflow_client.get_experiment_by_name(
                self.experiment_name).experiment_id

    @memoized_property
    def mlflow_run(self):
        return self.mlflow_client.create_run(self.mlflow_experiment_id)

    def mlflow_log_param(self, key, value):
        self.mlflow_client.log_param(self.mlflow_run.info.run_id, key, value)

    def mlflow_log_metric(self, key, value):
        self.mlflow_client.log_metric(self.mlflow_run.info.run_id, key, value)


if __name__ == "__main__":
    # Get and clean data
    df = pd.read_csv("../raw_data/final_data/final_data.csv")
    y = df["Kinderarmu"]
    X = df.drop(columns=["Kinderarmu", "geometry"])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    # Train and save model, locally and
    trainer = Trainer(X=X_train, y=y_train)
    trainer.set_experiment_name('xp2')
    trainer.run()
    score = trainer.evaluate(X_test, y_test)
    print(f"r2_score: {score}")
    trainer.save_model_locally()
