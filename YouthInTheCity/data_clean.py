#All functions were transfered from the notebook "Nicha-data-preproc",
##Don't forget to drop high-corr-features!!!
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

def get_full_data(filepath, filename):
    df = gpd.read_file(f"{filepath}/{filename}")
    return df

def clean_data(df):
    unused_column = "Unnamed: 0"
    if unused_column in df.keys():
        df = df.drop(axis=1, columns=["Unnamed: 0"])
    return df

def change_age_bin(df):
    """Change the bin of Population-Age (E)"""
    elist = ['E_EU1', 'E_E1U6', 'E_E6U15', 'E_E15U18',
                'E_E18U25','E_E25U55','E_E55U65','E_E65U80', 'E_E80U110']
    for e in elist:
        df[e] = df[e] * df["E_E"]
    df['E_U18'] = df['E_EU1'] + df['E_E1U6'] + df['E_E6U15'] + df['E_E15U18']
    df['E_E25U65'] = df['E_E25U55'] + df['E_E55U65']
    df['E_E65U110'] =  df['E_E65U80'] + df['E_E80U110']
    df.drop(columns=['E_E','E_EU1', 'E_E1U6', 'E_E6U15', 'E_E15U18','E_E25U55','E_E55U65','E_E65U80', 'E_E80U110'], inplace=True)
    return df

def change_building_bin(df):
    """Change the bin of Building-Age"""
    df['B_1940'] = df['bis_1900'] + df['x1901_1910'] + df['1911-1920'] + df['1921-1930']+ df['1930-1940']
    df['B_1941_1990'] = df['1941_1950'] + df['1951_1960'] + df['1961-1970'] + df['1971-1980'] + df['1980-1990']
    df['B_1991_2000'] = df['1991-2000'] + df['2001-2010'] + df['2010-2015']
    df.drop(columns=['bis_1900','x1901_1910','1911-1920', '1921-1930', '1930-1940',
    '1941_1950', '1951_1960','1961-1970', '1971-1980','1980-1990',
    '1991-2000', '2001-2010','2010-2015'], inplace=True)
    return df


def features_corr(df):
    """create list of pearson correlation"""
    corr = df.corr()
    corr_df = corr.unstack().reset_index() #Unstack correlation matrix
    corr_df.columns = ["feature_1", "feature_2", "correlation"] #Rename the columns
    corr_df.sort_values(by="correlation", ascending=False, inplace=True)
    corr_df = corr_df[corr_df["feature_1"] != corr_df["feature_2"]] #remove the self-corr
    return corr_df


def get_final_data(filepath, filename):
    """filepath is the direktory  + name of the data,
    and the filename of the data to be cleaned.
    The final data will be save in the same directory with the name --> final_data <--"""
    df = get_full_data(filepath, filename)
    df = clean_data(df)
    df = change_age_bin(df)
    df = change_building_bin(df)
    df.set_index('PLR_ID', inplace = True)
    df.rename(columns={'activities' : "economic",
        'activiti_1' :"education",'activiti_2' : "health_care",'activiti_3': "public_service"}, inplace=True)
    df.drop(columns=['ant_arbeit', 'ant_transf', 'ant_arbe_1', 'ant_tran_1', 'Kinderar_1',
        'aenderung_', 'wohnungsve','E_EM','E_EW', 'MH_EM', 'MH_EW', 'MH_U1', 'MH_1U6',
       'MH_6U15', 'MH_15U18', 'MH_18U25', 'MH_25U55', 'MH_55U65', 'MH_65U80',
       'MH_80U110','anteil_lei','wohnungs_2','Nummer', 'Name', 'EW','BEZ','BZR_ID',
       'PGR_ID', 'ew2015', 'index_left','mobility_b', 'mobility_1'], inplace = True)
    #drop the rows that missing y
    df = df[df['Kinderarmu'].notna()]
    df.to_csv(f"{filepath}/final_data.csv")
    df.to_file(f"{filepath}/final_data.shp")
    return print(f" See the final data with this shape {df.shape} csv and shp file in {filepath}")

if __name__ == '__main__':
    print("it is running")
    print(get_final_data("../raw_data/final_data", "full.shp"))
    print("its done")
