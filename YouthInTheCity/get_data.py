from create_api_gdf import query_to_gdf
from merge_bodp_data import  get_bodp_data
import geopandas as gpd
from query_names import query_keys
from create_api_gdf import feature_names, target_gdf, location, join_feature
import os

"""Merging all data into one GeoDataFrame"""

root_dir = os.path.dirname(os.path.dirname(__file__))
dir_path = os.path.join(root_dir,"YouthInTheCity", "data")

def get_final_gdf():
    api_features = query_to_gdf(query_keys=query_keys,
                 feature_names=feature_names,
                 target_gdf=target_gdf,
                 location=location,
                 join_feature=join_feature,
                 limit='')
    bodp_features = get_bodp_data()
    #api_features = gpd.read_file('/Users/Safia/code/Safiaaaaa/YouthInTheCity/YouthInTheCity/data/api_features.shp')
    #bodp_features = gpd.read_file('/Users/Safia/code/Safiaaaaa/YouthInTheCity/YouthInTheCity/data/bodp_features.shp')
    merged = api_features.merge(bodp_features.drop(columns='geometry'), on='PLR_ID')
    merged.to_file(os.path.join(dir_path, 'final_gdf.shp'))
    return merged

if __name__ == "__main__":
    print(get_final_gdf())
