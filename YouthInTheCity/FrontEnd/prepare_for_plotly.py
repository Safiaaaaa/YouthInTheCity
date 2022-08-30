import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gdp
import plotly.express as px
import json

def preparing_datas_for_plotly(geodata_source, regular_data_source, export_path):
    """Merge dataframe for the Plännungsräume name and transform shp file into geojson for plotly
    geodata_soure= '../raw_data/Maps/pr_2021.shp'
    regular_data_source = '../YouthInTheCity/data/final_gdf.csv'
    export_path= '../YouthInTheCity/data'"""
    geodf = gdp.read_file(geodata_source).to_crs('EPSG:4326') #read and change the crs system
    df = pd.read_csv(regular_data_source, dtype={'': str})
    df.drop(columns='Unnamed: 0', inplace=True)
    plr_df = pd.read_csv('../raw_data/Maps/pr_2021.csv')
    plr_df.drop(columns=["Unnamed: 0"], inplace=True)
    df_final = df.merge(plr_df)
    geodf.to_file(f"{export_path}/geodata_readytouse.geojson", driver='GeoJSON')
    with open(f"{export_path}/geodata_readytouse.geojson") as geofile:
        j_file = json.load(geofile)
    for f in j_file['features']:
        f['id'] = int(f['properties']['PLR_ID'])
    #Export the final plr geodata, ready to use for the plotly
    with open(f"{export_path}/geodata_readytouse.geojson", "w") as outfile:
        json.dump(j_file, outfile)
    #Export df_final
    df_final.to_csv(f"{export_path}/df_final.csv")
    return df_final, j_file


def plot_feature_on_map(df,geojson_file, locations = 'PLR_ID', color=None, hover_name='PLR_NAME',hover_data=['child_pov', 'unemployme']):
    """Features on plotly:
    - df = dataframe with values, geojson_file has to be prepared first
    - location = the key row that merge df anf geojson_file together
    - color = features that shown and labeled by color"""
    fig = px.choropleth_mapbox(
        data_frame = df,
        geojson=geojson_file,
        locations="PLR_ID",
        color=color,
        color_continuous_scale="Viridis",
        range_color=(df[color].max(), df[color].min()),
        mapbox_style="open-street-map",
        zoom=9,
        center={
            "lat": 52.52,
            "lon": 13.40
        },
        opacity=0.5,
        labels= {f"{color}: {color} amount"},
        hover_name= hover_name,
        hover_data=['child_pov', 'unemployme'])
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()
