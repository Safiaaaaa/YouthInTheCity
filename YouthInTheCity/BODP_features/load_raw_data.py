import os
import pandas as pd
import geopandas as gpd

""" Load maps and datasets from Berlin's Open Data Platform"""

def load_csvs():
    """
    Returns dataframes following dataframes on Planungraeume level: social index variables (child poverty, enemployment
    rate and rate of welfare beneficiaries), migration data, demographic data
    """
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    dir_path = os.path.join(root_dir,"raw_data", "social_data")
    file_names = os.listdir(dir_path)
    key_names = [file.replace(".csv", "") for file in file_names]
    data = {}
    for name, path in zip(key_names, file_names):
        if '.DS_Store' in name:
            continue
        elif name == 'social_index':
            data[name] = pd.read_csv(os.path.join(dir_path, path), sep=';', thousands='.', decimal=',')
        else:
            data[name] = pd.read_csv(os.path.join(dir_path, path), sep=';')
    return data

def load_maps():
    """
    Returns a dataframe with social index variables (child poverty, enemployment
    rate and rate of welfare beneficiaries) on Planungraeume level
    """
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    dir_path = os.path.join(root_dir,"raw_data", "maps")
    file_names = os.listdir(dir_path)
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
        maps[name] = gpd.read_file(os.path.join(dir_path, path))
    return maps

def get_maps_csv():
    csvs = load_csvs()
    maps = load_maps()
    merged = {**csvs, **maps}
    return merged

if __name__ == "__main__":
    print(get_maps_csv()['origin'])
