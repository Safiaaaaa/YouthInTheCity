import os
import pandas as pd
import geopandas as gpd

def load_social_data():
    """
    Returns dataframes following dataframes on Planungraeume level: social index variables (child poverty, enemployment
    rate and rate of welfare beneficiaries), migration data, demographic data
    """
    root_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(root_dir,"raw_data", "social_data")
    file_names = os.listdir(csv_path)
    key_names = [file.replace(".csv", "") for file in file_names]
    data = {}
    for name, path in zip(key_names, file_names):
        data[name] = pd.read_csv(os.path.join(csv_path, path))
    return data

def load_maps_and_csv():
    """
    Returns a dataframe with social index variables (child poverty, enemployment
    rate and rate of welfare beneficiaries) on Planungraeume level
    """
    root_dir = os.path.dirname(os.path.dirname(__file__))
    shp_path = os.path.join(root_dir,"raw_data", "maps")
    file_names = os.listdir(shp_path)
    key_names = []
    files = []
    extensions = ['cpg', 'dbf', 'prj', 'qmd', 'shx', 'sbn', 'sbx', 'xml', 'csv']
    maps = {}
    for file in file_names:
        if '.DS_Store' in file:
            continue
        if not any(ext in file for ext in extensions):
            key_names.append(file.replace(".shp", ""))
            files.append(file)
    for name, path in zip(key_names, files):
        maps[name] = gpd.read_file(os.path.join(shp_path, path))
    return maps

def merge_maps_csv():
    csvs = load_social_data()
    maps = load_maps_and_csv()
    merged = {**csvs, **maps}
    return merged

if __name__ == "__main__":
    print(merge_maps_csv())
