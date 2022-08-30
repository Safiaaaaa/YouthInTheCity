import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gdp
import plotly.express as px

'''
# Youth in the City RESULTs
'''

option = st.selectbox(
     'Which feature do you like to see on Berlin Maps',
     ('PLR_ID', 'public_tra', 'eating', 'culture', 'community', 'health_car',
       'public_ser', 'education', 'schools', 'universiti', 'kindergart',
       'outdoor_fa', 'outdoor_le', 'night_life', 'water', 'E_E', 'E_EM',
       'E_EW', 'E_EU1', 'E_E1U6', 'E_E6U15', 'E_E15U18', 'E_E18U25',
       'E_E25U55', 'E_E55U65', 'E_E65U80', 'E_E80U110', 'MH_E', 'MH_EM',
       'MH_EW', 'MH_U1', 'MH_1U6', 'MH_6U15', 'MH_15U18', 'MH_18U25',
       'MH_25U55', 'MH_55U65', 'MH_65U80', 'MH_80U110', 'ave_rent',
       'dyn_wel_po', 'welf_po', 'social_hou', 'public_hou', 'dyn_ew',
       'five_y_pls', 'rent_to_pr', 'dyn_r_to_p', 'sales', 'dyn_sales', 'EW',
       'unemployme', 'welfare', 'child_pov', 'dyn_unempl', 'dyn_welfar',
       'dyn_child', 'noise', 'air', 'green', 'bio', 'x_bis_1900', 'x1901_1910',
       'x1911_1920', 'x1921_1930', 'x1931_1940', 'x1941_1950', 'x1951_1960',
       'x1961_1970', 'x1971_1980', 'x1981_1990', 'x1991_2000', 'x2001_2010',
       'x2011_2015', 'ew2015'))

st.write(f" Here is the Maps for  {option} in Berlin")

@st.cache
def get_plotly_data():
    geojson_path = '/Users/nicha/code/Safiaaaaa/YouthInTheCity/YouthInTheCity/data/plr_final.geojson'
    df = pd.read_csv('/Users/nicha/code/Safiaaaaa/YouthInTheCity/YouthInTheCity/data/final_gdf.csv', dtype={'': str})
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
        opacity=0.5,
        labels= {f"{color_option}: {color_option} amount"})
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

st.plotly_chart(fig)
