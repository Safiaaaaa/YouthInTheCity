import os
import pandas as pd

def load_social_index():
    """
    Returns a dataframe with social index variables (child poverty, enemployment
    rate and rate of welfare beneficiaries) on Planungraeume level
    """

    root_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(root_dir,"social_index_2021", "csv")


        file_names = os.listdir(csv_path)
        key_names = [file.replace(".csv", "").replace("_dataset","").replace("olist_", "") for file in file_names]
        data = {}
        for name, path in zip(key_names, file_names):
            data[name] = pd.read_csv(os.path.join(csv_path, path))
        return data
