import pandas as pd
import numpy as np
import geopandas as gpd
import sys
import os
# getting the name of the directory where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
# Getting the parent directory name where the current directory is present.
parent = os.path.dirname(current)
# adding the parent directory to the sys.path.
sys.path.append(parent)
from OSM_features.OSM_query import query_params_osm
#from OSM_features.query_names import query_keys, feature_names, target_gdf, join_feature, location
import time
import os

"""Transforming API features from csv to geodataframe,
adapting projection and coordinates,
adding 500m buffers aroung the points"""

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
dir_path = os.path.join(root_dir,"raw_data", "output_maps")

def open_filter(df):
    """transforms dataframe into a geodataframe and
    filters the results to ignore points outside of Berlin"""

    df['lat_num'] = df.loc[:, 'lat'].astype(float)
    df['lon_num'] = df.loc[:, 'lon'].astype(float)
    geo_df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat),
                              crs='epsg:4326')
    geo_df_filtered = geo_df[(geo_df.lat_num > 50) & (geo_df.lon_num > 12)]
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
    query_k_failed = []
    query_n_failed = []

    for key, name in zip(query_keys, feature_names):
        new_querie  = query_params_osm(location=location, keys=key, limit=limit)
        if new_querie != None:
            df = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
            geo_df = open_filter(df)
            merged_df = spatial_intersect(geo_df, merged_df, join_feature, name)
        else:
            print(f' ------ {name} FAILED ------')
            query_k_failed.append(key)
            query_n_failed.append(name)
        time.sleep(30)

    if query_k_failed:
        for key, name in zip(query_k_failed, query_n_failed):
            new_querie  = query_params_osm(location=location, keys=key, limit=limit)
            if new_querie != None:
                df = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
                geo_df = open_filter(df)
                merged_df = spatial_intersect(geo_df, merged_df, join_feature, name)
            else:
                print(f' ------ {name} FAILED ------')

    merged_df.replace(np.nan, 0, inplace=True)
    merged_df.to_file(os.path.join(dir_path, 'api_features.shp'))
    return merged_df


if __name__ == '__main__':

    #print(query_to_gdf(query_keys=query_keys,
     #            feature_names=feature_names,
      #           target_gdf=target_gdf,
       #          location=location,
        #         join_feature=join_feature,
         #        limit=''))
    print(sys.path)
