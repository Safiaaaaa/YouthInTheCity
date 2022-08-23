import pandas as pd
import numpy as np
import geopandas as gpd
from OSM_query import query_params_osm
from query_names import query_keys
import os
import pygeos
import rtree

"""Transforming API features from csv to geodataframe,
adapting projection and coordinates,
adding 500m buffers aroung the points"""

root_dir = os.path.dirname(os.path.dirname(__file__))
dir_path = os.path.join(root_dir,"raw_data", "maps")
target_gdf = gpd.read_file(os.path.join(dir_path, 'pr_2021.shp'))
join_feature = 'PLR_ID'
location = 'Berlin'
feature_names = ['public_transport', 'eating', 'night_life', 'culture', 'community',
                    'health_care', 'public_service', 'education', 'schools',
                    'universities', 'kindergarten', 'outdoor_facilities',
                    'outdoor_leisure', 'water']

def open_filter(df):
    """transforms dataframe into a geodataframe and
    filters the results to ignore points outside of Berlin"""

    df['lat_num'] = df.loc[:, 'lat'].astype(float)
    df['lon_num'] = df.loc[:, 'lon'].astype(float)
    geo_df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat),
                              crs='epsg:4326')
    geo_df_filtered = geo_df[(geo_df.lat_num>50) & (geo_df.lon_num > 12)]
    geo_df_filtered.to_crs(crs='epsg:25833', inplace=True)
    geo_df_filtered['buffer'] = geo_df_filtered.buffer(500)
    geo_df_filtered.set_geometry('buffer', inplace=True)

    return geo_df_filtered

def spatial_intersect(df, target, join_feature, feature_name):
    '''spatial join between feature geo_df and Planungsräume'''

    intersect = df.sjoin(target, how='left', predicate = 'intersects')
    feature_amount = intersect.groupby(by=join_feature).size().reset_index()
    feature_amount.columns = [join_feature, feature_name]
    merged = target.merge(feature_amount, on=join_feature, how= 'left')

    return merged

def query_to_gdf(query_keys, feature_names, target_gdf, location, join_feature, limit=''):
    """sends API query to get all features and returns a geodataframe with the
    amount of feature per Planungsraum"""

    merged_df = target_gdf

    for key, name in zip(query_keys, feature_names):
        new_querie  = query_params_osm(location=location, keys=key, limit=limit)
        df = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
        geo_df = open_filter(df)
        merged_df = spatial_intersect(geo_df, target_gdf, join_feature, name)

    return merged_df

if __name__ == '__main__':

    print(query_to_gdf(query_keys=query_keys,
                 feature_names=feature_names,
                 target_gdf=target_gdf,
                 location=location,
                 join_feature=join_feature))
