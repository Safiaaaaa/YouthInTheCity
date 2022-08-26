import pandas as pd
import query_names
from query_names import feature_names, query_keys, feature_names, target_gdf, join_feature, location
from OSM_query import query_params_osm
from create_api_gdf import open_filter, spatial_intersect
import numpy as np
import os
import time

"""Loading API responses as CSVs"""

root_dir = os.path.dirname(os.path.dirname(__file__))
dir_path = os.path.join(root_dir,"YouthInTheCity", "data")


def query_to_csv():
    """sends API query to get all features and returns a geodataframe with the
    amount of feature per Planungsraum"""

    query_k_failed = []
    query_n_failed = []

    for key, name in zip(query_keys, feature_names):
        time.sleep(10)
        merged_df = target_gdf
        new_querie  = query_params_osm(location=location, keys=key, limit='')
        if new_querie != None:
            df = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
            geo_df = open_filter(df)
            merged_df = spatial_intersect(geo_df, merged_df, join_feature, name)
            merged_df.replace(np.nan, 0, inplace=True)
            merged_df.to_csv(os.path.join(dir_path, f'{name}.csv'))
        else:
            print(f' ------ {name} FAILED ------')
            query_k_failed.append(key)
            query_n_failed.append(name)

    time.sleep(30)
    for key, name in dict(zip(query_k_failed, query_n_failed)):
        merged_df = target_gdf
        new_querie  = query_params_osm(location=location, keys=key, limit='')
        if new_querie != None:
            df = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
            geo_df = open_filter(df)
            merged_df = spatial_intersect(geo_df, merged_df, join_feature, name)
            merged_df.replace(np.nan, 0, inplace=True)
            merged_df.to_csv(os.path.join(dir_path, f'{name}.csv'))
        else:
            print(f' ------ {name} FAILED 2nd time ------')

if __name__ == "__main__":
    #print(query_to_csv())
    new_querie  = query_params_osm(location=location, keys= query_keys[0], limit='')
    if new_querie != None:
        df = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
        df.to_csv('YouthInTheCity/data/publi_trans_all')
