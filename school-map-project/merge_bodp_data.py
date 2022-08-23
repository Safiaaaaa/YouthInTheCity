import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import pygeos
import rtree
from fiona import BytesCollection
from tobler.area_weighted import area_interpolate
from tobler.dasymetric import masked_area_interpolate
from load_raw_data import get_maps_csv

"""Functions to merge data from Berlin's open data platform"""


mig_data = get_maps_csv()['migration_data']
gen_data = get_maps_csv()['demo_data']
social_index = get_maps_csv()['social_index']
pr_2020 = get_maps_csv()['pr_2020']
pr_2020['RAUMID'] = pd.to_numeric(pr_2020['Plr_Nummer'])
pr_2021 = get_maps_csv()['pr_2021']
filtered_blocks = get_maps_csv()['filtered_blocks']
housing_data = get_maps_csv()['housing_data']

def create_demo_mig_gdf():
    """returns a gdf with migration and demographic data on planungraum level 2021"""

    # Merge demo and migration df
    merged_data = gen_data.drop(
    columns=['BEZ', 'PGR', 'BZR', 'PLR', 'STADTRAUM', 'E_E00_01', 'E_E01_02', 'E_E02_03', 'E_E03_05',
       'E_E05_06', 'E_E06_07', 'E_E07_08', 'E_E08_10', 'E_E10_12', 'E_E12_14',
       'E_E14_15', 'E_E15_18', 'E_E18_21', 'E_E21_25', 'E_E25_27', 'E_E27_30',
       'E_E30_35', 'E_E35_40', 'E_E40_45', 'E_E45_50', 'E_E50_55', 'E_E55_60',
       'E_E60_63', 'E_E63_65', 'E_E65_67', 'E_E67_70', 'E_E70_75', 'E_E75_80',
       'E_E80_85', 'E_E85_90', 'E_E90_95', 'E_E95_110']).merge(
    mig_data.drop(
    columns=['ZEIT', 'BEZ', 'PGR', 'BZR', 'PLR', 'STADTRAUM', 'MH_E00_01', 'MH_E01_02', 'MH_E02_03', 'MH_E03_05',
       'MH_E05_06', 'MH_E06_07', 'MH_E07_08', 'MH_E08_10', 'MH_E10_12',
       'MH_E12_14', 'MH_E14_15', 'MH_E15_18', 'MH_E18_21', 'MH_E21_25',
       'MH_E25_27', 'MH_E27_30', 'MH_E30_35', 'MH_E35_40', 'MH_E40_45',
       'MH_E45_50', 'MH_E50_55', 'MH_E55_60', 'MH_E60_63', 'MH_E63_65',
       'MH_E65_67', 'MH_E67_70', 'MH_E70_75', 'MH_E75_80', 'MH_E80_85',
       'MH_E85_90', 'MH_E90_95', 'MH_E95_110'])
)
    # merge df with planungsräume 2020 geodatagrame (449 rows)
    demo_gdf = pr_2020[['RAUMID', 'BEZNAME','PLRNAME', 'geometry']].merge(
         merged_data, on='RAUMID')

    # interpolate merged gdf into planungsräume 2021 (542 rows)
    interpolate = area_interpolate(
        source_df=demo_gdf,
        target_df= pr_2021,
        extensive_variables=['E_E', 'E_EM', 'E_EW', 'E_EU1', 'E_E1U6', 'E_E6U15',
            'E_E15U18', 'E_E18U25', 'E_E25U55', 'E_E55U65', 'E_E65U80', 'E_E80U110',
            'MH_E', 'MH_EM', 'MH_EW', 'MH_U1', 'MH_1U6', 'MH_6U15', 'MH_15U18',
            'MH_18U25', 'MH_25U55', 'MH_55U65', 'MH_65U80', 'MH_80U110'])

    # merge with planungsräume 2021 to add the planungsraum identifier
    merged_data_2021 = pr_2021[['PLR_ID', 'PLR_NAME', 'geometry']].merge(interpolate, on='geometry')

    return merged_data_2021

def create_housing_gdf():
    """ Returns a geodatagrame on planungsräume 2021 with housing data"""

    # change data type to numerical
    columns = ['angebotsmi', 'aenderung_', 'anteil_lei',
       'anteil_soz', 'anteil_sta', 'entwicklun', 'wohndauer', 'wohnungsum',
       'wohnungs_1', 'wohnungsve', 'wohnungs_2']
    for c in columns:
        housing_data[f'{c}'] = pd.to_numeric(housing_data[f'{c}'])

    # interpolate data to planungsräume level
    interpolate = area_interpolate(
    source_df=housing_data,
    target_df=pr_2021,
    intensive_variables=['angebotsmi', 'aenderung_', 'anteil_lei',
       'anteil_soz', 'anteil_sta', 'entwicklun', 'wohndauer', 'wohnungsum',
       'wohnungs_1', 'wohnungsve', 'wohnungs_2'])
    merged_data_2021 = pr_2021[['PLR_ID', 'PLR_NAME', 'geometry']].merge(interpolate, on='geometry')

    return merged_data_2021

def create_social_gdf():
    """ Returns a geodataframe with the social index (unemployment rate, social
    welfare beneficiaries and child poverty on planungsräume 2021 level"""
    columns = ['EW', 'ant_arbeitslose', 'ant_transfer',
       'Kinderarmut', 'ant_arbeitslose_dyn', 'ant_transfer_dyn',
       'Kinderarmut_dyn']
    for c in columns:
        social_index[f'{c}'] = pd.to_numeric(social_index[f'{c}'])
    return social_index



if __name__ == '__main__':
    print(create_social_gdf())
