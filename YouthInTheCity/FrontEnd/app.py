import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gdp
import plotly.express as px

df = pd.read_csv('../data/labeled.csv', dtype={'': str})
'''
# Youth in the City RESULTs
'''

option = st.selectbox(
     'Which feature do you like to see on Berlin Maps?',
     ('public_tra', 'eating', 'culture', 'community', 'health_car',
       'public_ser', 'education', 'schools', 'universiti', 'kindergart',
       'outdoor_fa', 'outdoor_le', 'night_life', 'water', 'ave_rent',
       'social_hou', 'public_hou', 'dyn_ew', 'five_y_pls', 'dyn_sales',
       'child_pov', 'dyn_unempl', 'noise', 'air', 'green', 'bio', 'B_age',
       'mig_rate', 'label', 'PLR_NAME', 'BZR_NAME'))

st.write(f" Here is the Maps for {option} in Berlin")

@st.cache
def get_plotly_data():
    geojson_path = '../data/geodata_readytouse.geojson'
    df = pd.read_csv('../data/labeled.csv', dtype={'': str})
    with open(geojson_path) as geofile:
        j_file = json.load(geofile)
    #for f in j_file['features']:
        #f['id'] = int(f['properties']['PLR_ID'])

    return df, j_file

df, geojson_file = get_plotly_data()

color_option = str(option)

fig = px.choropleth_mapbox(
        data_frame = df,
        geojson= geojson_file,
        locations="PLR_ID",
        color=color_option,
        color_continuous_scale="Viridis",
        range_color=(df[color_option].max(), df[color_option].min()),
        mapbox_style="open-street-map",
        zoom=9,
        center={
            "lat": 52.52,
            "lon": 13.40
        },
        labels= {f"{color_option}: {color_option} amount"},
        hover_name='PLR_NAME',
        hover_data=['child_pov', 'mig_rate','dyn_unempl'])
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

st.plotly_chart(fig)


multi_option = st.multiselect(
     'Which feature do you like to see by hovering your mouse?',
     ('public_tra', 'eating', 'culture', 'community', 'health_car',
       'public_ser', 'education', 'schools', 'universiti', 'kindergart',
       'outdoor_fa', 'outdoor_le', 'night_life', 'water', 'ave_rent',
       'social_hou', 'public_hou', 'dyn_ew', 'five_y_pls', 'dyn_sales',
       'child_pov', 'dyn_unempl', 'noise', 'air', 'green', 'bio', 'B_age',
       'mig_rate', 'label', 'PLR_NAME', 'BZR_NAME'))
st.write(f" Here is the clustering result")


hover_datas = multi_option

fig = px.choropleth_mapbox(
        data_frame = df,
        geojson= geojson_file,
        locations="PLR_ID",
        color="label",
        #color_continuous_scale="Rainbow",
        #range_color=(df[color_option].max(), df[color_option].min()),
        mapbox_style="open-street-map",
        zoom=9,
        center={
            "lat": 52.52,
            "lon": 13.40
        },
        labels= {f"{color_option}: {color_option} amount"},
        hover_name='PLR_NAME',
        hover_data= ['child_pov'] + hover_datas)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},coloraxis_colorbar=dict(
    title="clustering",
    thicknessmode="pixels",
    lenmode="pixels",
    yanchor="top",y=1,
    ticks="outside",
    tickvals=[0,1,2,3,4],
    ticktext=["0", "1", "2", "3"],
    dtick=4
))

st.plotly_chart(fig)
