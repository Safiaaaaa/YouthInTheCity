import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, make_pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, FunctionTransformer
from sklearn.linear_model import Ridge

def load_final_data(filepath):
    df = gpd.read_file(filepath)
    return df

X = data.drop(columns=["days_until_delivery"])
y = data[["days_until_delivery"]]

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)
#make volumn
volumn = FunctionTransformer(lambda data: pd.DataFrame(data["product_weight_g"] * data["product_length_cm"]* data["product_height_cm"]))
#impute the scale for num variables
num_transformer = Pipeline([("scaler",MinMaxScaler())])
#impute the onehotcoder for the cat varibles
cat_transformer = Pipeline([
    ("encoder",OneHotEncoder(handle_unknown="ignore", sparse=True))])
#Paralelize both varibles kinds
preprocessor = ColumnTransformer([
    ("num_tr", num_transformer,['product_weight_g', 'product_length_cm', 'product_height_cm',
       'product_width_cm']),
    ("cat_tr", cat_transformer,["customer_state","seller_state"])
])
union = FeatureUnion([("preproc",preprocessor),
                     ("volumn",make_pipeline(volumn, MinMaxScaler()))])
pipe = make_pipeline(union,Ridge())
pipe

import joblib
from termcolor import colored
import mlflow
from TaxiFareModel.data import get_data_from_gcp, clean_data
from TaxiFareModel.encoders import TimeFeaturesEncoder, DistanceTransformer
from TaxiFareModel.gcp import storage_upload
from TaxiFareModel.utils import compute_rmse
from TaxiFareModel.params import MLFLOW_URI, EXPERIMENT_NAME, BUCKET_NAME, MODEL_VERSION, MODEL_VERSION
from memoized_property import memoized_property
from mlflow.tracking import MlflowClient
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler



class Trainer(object):
    def __init__(self, X, y):
        """
            X: pandas DataFrame
            y: pandas Series
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
        dist_pipe = Pipeline([
            ('dist_trans', DistanceTransformer()),
            ('stdscaler', StandardScaler())
        ])
        time_pipe = Pipeline([
            ('time_enc', TimeFeaturesEncoder('pickup_datetime')),
            ('ohe', OneHotEncoder(handle_unknown='ignore'))
        ])
        preproc_pipe = ColumnTransformer([
            ('distance', dist_pipe, [
                "pickup_latitude",
                "pickup_longitude",
                'dropoff_latitude',
                'dropoff_longitude'
            ]),
            ('time', time_pipe, ['pickup_datetime'])
        ], remainder="drop")

        self.pipeline = Pipeline([
            ('preproc', preproc_pipe),
            ('linear_model', LinearRegression())
        ])

    def run(self):
        self.set_pipeline()
        self.mlflow_log_param("model", "Linear")
        self.pipeline.fit(self.X, self.y)

    def evaluate(self, X_test, y_test):
        """evaluates the pipeline on df_test and return the RMSE"""
        y_pred = self.pipeline.predict(X_test)
        rmse = compute_rmse(y_pred, y_test)
        self.mlflow_log_metric("rmse", rmse)
        return round(rmse, 2)

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
    N = 100
    df = get_data_from_gcp(nrows=N)
    df = clean_data(df)
    y = df["fare_amount"]
    X = df.drop("fare_amount", axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    # Train and save model, locally and
    trainer = Trainer(X=X_train, y=y_train)
    trainer.set_experiment_name('xp2')
    trainer.run()
    rmse = trainer.evaluate(X_test, y_test)
    print(f"rmse: {rmse}")
    trainer.save_model_locally()
    storage_upload()
