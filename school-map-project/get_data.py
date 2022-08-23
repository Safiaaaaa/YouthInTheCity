from get_csv import get_all
from create_api_gdf import query_to_gdf
from merge_bodp_data import  get_bodp_data
import geopandas as gpd

"""Merging all data into one GeoDataFrame"""

def get_final_gdf():
    api_features = query_to_gdf()
    bodp_features = get_bodp_data()
    merged = bodp_features.merge(api_features, on='PLR_ID')
    merged.to_file('data/final_gdf.shp')
    return merged

if __name__ == "__main__":
    print(get_final_gdf())
