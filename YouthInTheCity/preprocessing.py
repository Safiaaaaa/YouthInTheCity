import geopandas as gpd
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.impute import KNNImputer
from get_data import get_final_gdf

knn=KNNImputer()
robust = RobustScaler()

""" Drops unnecessary features and transforms some (e.g. absolute numbers to rate)"""
#----> muss noch pipeline hinzufügen / pb index reset ?
#def building_age_main(gdf):
#   gdf['total_buildings'] = np.sum(gdf[['x_bis_1900','x1901_1910',
#       'x1911_1920', 'x1921_1930', 'x1931_1940', 'x1941_1950', 'x1951_1960',
#       'x1961_1970', 'x1971_1980', 'x1981_1990', 'x1991_2000', 'x2001_2010',
#       'x2011_2015']], axis=1)
#    gdf['B_1940'] = (gdf['x_bis_1900'] + gdf['x1901_1910'] + gdf['x1911_1920'] + gdf['x1921_1930']+ gdf['x1931_1940'])/ gdf['total_buildings']
#    gdf['B_1941_1990'] = (gdf['x1941_1950'] + gdf['x1951_1960'] + gdf['x1961_1970'] + gdf['x1971_1980'] + gdf['x1981_1990'])/ gdf['total_buildings']
#    gdf['B_1991_2015'] = (gdf['x1991_2000'] + gdf['x2001_2010'] + gdf['x2011_2015'])/ gdf['total_buildings']
#    gdf['B_age'] = gdf[['B_1940','B_1941_1990','B_1991_2015']].idxmax(axis=1)
#    return gdf

#def compute_mh_rate(gdf):
#    gdf['mig_rate'] = gdf.MH_E / gdf.E_E
#    return gdf

def drop_y_na(gdf):
    """ drops rows with missing target"""
    gdf = gdf[gdf['child_pov'].notna()].reset_index(drop=True)
    return gdf

def drop_features_regression(gdf):
    """ drops redundant features / those which correlate too much """
    gdf.drop(columns=['MH_E', 'MH_EM', 'MH_EW', 'MH_U1', 'MH_1U6',
            'MH_6U15', 'MH_15U18', 'MH_18U25','MH_25U55', 'MH_55U65',
            'MH_65U80', 'MH_80U110','E_E', 'E_EM','E_EW', 'E_EU1',
            'E_E1U6', 'E_E6U15', 'E_E15U18', 'E_E18U25','E_E25U55',
            'E_E55U65', 'E_E65U80', 'E_E80U110', 'dyn_wel_po', 'welf_po',
            'rent_to_pr', 'dyn_r_to_p', 'sales', 'EW', 'unemployme',
            'welfare', 'x_bis_1900', 'x1901_1910','x1911_1920', 'x1921_1930',
            'x1931_1940', 'x1941_1950', 'x1951_1960','x1961_1970', 'x1971_1980',
            'x1981_1990', 'x1991_2000', 'x2001_2010','x2011_2015', 'ew2015',
            'dyn_welfar','dyn_child', 'total_buil', 'B_1940', 'B_1941_199',
            'B_1991_201', 'B_age'], inplace = True)
    return gdf

def drop_features_clustering(gdf):
    """ drops unnecessary features """
    gdf.drop(columns=['MH_E', 'MH_EM', 'MH_EW', 'MH_U1', 'MH_1U6',
            'MH_6U15', 'MH_15U18', 'MH_18U25','MH_25U55', 'MH_55U65',
            'MH_65U80', 'MH_80U110','E_E', 'E_EM','E_EW','EW','x_bis_1900', 'x1901_1910','x1911_1920', 'x1921_1930',
            'x1931_1940', 'x1941_1950', 'x1951_1960','x1961_1970', 'x1971_1980',
            'x1981_1990', 'x1991_2000', 'x2001_2010','x2011_2015', 'ew2015','kindergart', 'schools',
                 'vegpm10', 'change',], inplace = True)
    return gdf


def get_reg_gdf(gdf):
    """ drops columns and rows, imputes missing values, set PLR_ID as index"""
    gdf = drop_y_na(drop_features_regression(gdf)).reset_index(drop=True)
    X = gdf.drop(columns=['PLR_ID','geometry', 'BZR_NAME', 'child_pov'])
    columns = list(X.columns)
    X_transformed = knn.fit_transform(X)
    X_transformed = pd.DataFrame(X_transformed)
    X_transformed.columns = columns
    for c in columns:
        gdf[c] = X_transformed.loc[:,c]
    gdf = gdf.set_index('PLR_ID')
    return gdf

def get_clust_gdf(gdf):
    """ drops columns and rows, imputes missing values, scales features and
    set PLR_ID as index"""

    gdf = drop_y_na(drop_features_clustering(gdf)).reset_index(drop=True)
    X = gdf.drop(columns=['PLR_ID','geometry', 'BZR_NAME', 'child_pov',  'B_age'])
    columns = list(X.columns)
    X_imputed = knn.fit_transform(X)
    X_transformed = robust.fit_transform(X_imputed)
    X_transformed = pd.DataFrame(X_transformed)
    X_transformed.columns = columns
    for c in columns:
        gdf[c] = X_transformed.loc[:,c]
    gdf = gdf.set_index('PLR_ID')
    return gdf


if __name__ == '__main__':
    #get_reg_gdf(gpd.read_file(
    #    'raw_data/output_maps/merged_gdf.shp')).to_file(
    #        'YouthInTheCity/data/regression_gdf.shp')
    #get_clust_gdf(gpd.read_file(
    #    'raw_data/output_maps/merged_gdf.shp')).to_file(
    #        'YouthInTheCity/data/cluster_gdf.shp')

    get_reg_gdf(get_final_gdf()).to_file(
            'YouthInTheCity/data/regression_gdf.shp')
    get_clust_gdf(get_final_gdf()).to_file(
            'YouthInTheCity/data/cluster_gdf.shp')
