import pandas as pd
import numpy as np
import geopandas as gpd
import pygeos
import rtree

"""transforming API features from csv to geodataframe
and adapting projection and coordinates"""


def open_filter(csv_path):
    """opens csv file as dataframe, transforms it into a geodataframe and
    filters the results to ignore points outside of Berlin"""
    df = pd.read_csv(csv_path)
    df['lat_num'] = df.loc[:, 'lat'].astype(float)
    df['lon_num'] = df.loc[:, 'lon'].astype(float)
    geo_df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs='epsg:4326')
    geo_df_filtered = geo_df[(geo_df.lat_num>50) & (geo_df.lon_num > 12)]
    geo_df_filtered.to_crs(crs='epsg:25833', inplace=True)
    return geo_df_filtered

if __name__ == '__main__':
    print(open_filter('data/api_features/night.csv'))
