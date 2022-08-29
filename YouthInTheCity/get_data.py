import geopandas as gpd
import os
from OSM_features.create_api_gdf import query_to_gdf
from OSM_features.query_names import feature_names, query_keys, feature_names, target_gdf, join_feature, location
from BODP_features.merge_bodp_data import get_bodp_data


"""Merging all data into one GeoDataFrame"""

root_dir = os.path.dirname(os.path.dirname(__file__))
dir_path = os.path.join(root_dir,"raw_data", "output_maps")

def get_final_gdf():
    api_features = query_to_gdf(query_keys=query_keys,
                 feature_names=feature_names,
                 target_gdf=target_gdf,
                 location=location,
                 join_feature=join_feature,
                 limit='')
    bodp_features = get_bodp_data()
    #api_features = gpd.read_file(
    #    os.path.join('raw_data', 'output_maps' ,'api_features1.shp'))
    api_features['PLR_ID'] = api_features['PLR_ID'].astype(int)
    #bodp_features = gpd.read_file(
    #os.path.join(dir_path, 'bodp_features.shp')
    merged = api_features.merge(
        bodp_features.drop(columns='geometry'), on='PLR_ID')
    #merged.to_file(os.path.join(dir_path, 'merged_gdf.shp'))
    return merged

if __name__ == "__main__":
    get_final_gdf()
