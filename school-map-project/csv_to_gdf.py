import pandas as pd
import numpy as np
import geopandas as gpd
from OSM_query import query_params_osm
"""from query_names import public_transport, eating, night_life, culture, community, health_care, public_service, education, schools, universities, kindergarten, outdoor_facilities, outdoor_leisure, water
"""
from query_names import query_keys
import os
import pygeos
import rtree

"""transforming API features from csv to geodataframe
and adapting projection and coordinates"""



def open_filter(df):
    """transforms dataframe into a geodataframe and
    filters the results to ignore points outside of Berlin"""
    df['lat_num'] = df.loc[:, 'lat'].astype(float)
    df['lon_num'] = df.loc[:, 'lon'].astype(float)
    geo_df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat),
                              crs='epsg:4326')
    geo_df_filtered = geo_df[(geo_df.lat_num>50) & (geo_df.lon_num > 12)]
    geo_df_filtered.to_crs(crs='epsg:25833', inplace=True)
    return geo_df_filtered

def spatial_intersect(df, target, join_feature, feature_name):
    nearest = df.sjoin(target, how='left', predicate = 'intersects')
    feature_df = nearest.groupby(by=join_feature).size().reset_index()
    feature_df.columns = [join_feature, feature_name]
    merged = target.merge(feature_df, on=join_feature, how= 'left')
    return merged


"""for key in query_keys:
    new_querie  = query_params_osm(location = 'Berlin', keys=key)
    df_public_transport = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]"""


if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.dirname(__file__))
    dir_path = os.path.join(root_dir,"raw_data", "maps")
    target = gpd.read_file(os.path.join(dir_path, 'pr_2021.shp'))
    join_feature = 'PLR_ID'
    location = 'Berlin'
    feature_names = ['public_transport', 'eating', 'night_life', 'culture', 'community',
                     'health_care', 'public_service', 'education', 'schools',
                     'universities', 'kindergarten', 'outdoor_facilities',
                     'outdoor_leisure', 'water']
    query_keys_short = query_keys[1:3]
    feature_names_short = feature_names[1:5]

    merged_df = target

    for key, name in zip(query_keys_short, feature_names_short):
        new_querie  = query_params_osm(location = location, keys=key)
        df = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
        geo_df = open_filter(df)
        merged_df = spatial_intersect(geo_df, target, join_feature, name)

    print(merged_df.columns)
