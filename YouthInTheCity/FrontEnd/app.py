import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gdp
import plotly.express as px

df = pd.read_csv('../data/labeled.csv', dtype={'': str})
df_fullname = pd.read_csv('../data/full_name.csv', dtype={'': str})
df_final = pd.read_csv('../data/fullcleaned.csv', dtype={'': str})

'''
# Youth in the City RESULTs
'''
def get_columnname(option, df):
    df_filtern = df[df.fullname == option]
    return df_filtern.column_name.values[0]
def get_fullname(column_name, df):
    df_filtern = df[df.column_name == column_name]
    return df_filtern.fullname.values

option = st.selectbox('Which feature do you like to see on Berlin Maps?',
     ('Migration in %',
 'Unemployment in %',
 'Welfare beneficiaries in %',
 'Child poverty in %',
 'Dynamic of unemployment in %',
 'Dynamic of welfare in %',
 'Dynamic of child poverty in %',
 'Rent in €/m2',
 'Social housing in %',
 'The less-profit housing in %',
 'Tranformation public to private appartment in %',
 'Dynamic of public/private transformation  in %',
 'Aparment sale in %',
 'Dynamic of sales between 2015 and 2020',
 'The people live in this area more than 5 years in %',
 'Number of all public transports',
 'Number of restaurants exc. fast food',
 'Number of museums, art centers, cinemas, theaters, etc.',
 'Number of ngos, social and community centers, etc.',
 'Number of hospital, clinics, pharmacies, etc.',
 'Number of fire station, police, post box, townhall, etc.',
 'Number of langague and music schools, edu institutions',
 'Number of schools',
 'Number of universities ',
 'Number of kindergartens',
 'Number of picnic tables, benches, bbq, water points, etc.',
 'Number of swimming pool, park, playground, etc.',
 'Number of bars, pubcs, nightclubs, etc.',
 'Number of lake, rivers, etc.',
 'Building age older than 1940 in %',
 'Building age between 1941-1991 in %',
 'Building age between 1991-2001 in %',
 'Green space in m2',
 'Number of other types of schools',
 'Number of vocational school',
 'Number of primary school',
 'Number of gymnasium',
 'Number of other secondary school',
 'Number of private school',
 'Number of school for children with special needs',
 'Number of kindergartens ',
 'Number of rail / u-bahn / s-bahn, tram stations'))

st.write(f" Here is {option} in each Planningarea")

@st.cache
def get_plotly_data():
    geojson_path = '../data/geodata_readytouse.geojson'
    df = pd.read_csv('../data/labeled.csv', dtype={'': str})
    with open(geojson_path) as geofile:
        j_file = json.load(geofile)
    return df, j_file

df, geojson_file = get_plotly_data()

color = get_columnname(str(option), df_fullname)
fig = px.choropleth_mapbox(
        data_frame = df_final,
        geojson=geojson_file,
        locations="PLR_ID",
        color=color,
        color_continuous_scale="Viridis",
        range_color=(df_final[color].max(), df_final[color].min()),
        mapbox_style="open-street-map",
        zoom=9,
        center={
            "lat": 52.52,
            "lon": 13.40
        },
        opacity=0.5,
        #labels= {f"{color}: {color} amount"},
        hover_name='PLR_NAME',
        hover_data={'PLR_ID':False, 'child_pov':True, color: True}
        )
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()

st.plotly_chart(fig)

#hover_data = {'a':True,'b':True, 'c':True, 'id':False}
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
        #labels= {f"{color_option}: {color_option} amount"},
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
