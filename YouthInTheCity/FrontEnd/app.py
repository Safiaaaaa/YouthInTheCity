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

option = st.selectbox('Which feature do you like to see on Berlin map?',
     ('Population with migration background in %',
 'Unemployment in %',
 'Welfare beneficiaries in %',
 'Child poverty in %',
 'Dynamic of unemployment in % (2018 to 2020)',
 'Dynamic of welfare in % (2018 to 2020)',
 'Dynamic of child poverty in % (2018 to 2020)',
 'Average advertised rent in €/m2',
 'Social housing in %',
 'Share of municipal housing companies in the housing stock in %',
 'Conversion of multi-family houses into condos per 1000 apartments',
 'Dynamic of condo conversion in % (2015 to 2020)',
 'Apartments sale per 1000 apartments ',
 'Dynamic of apartment sales in % (2015 to 2020)',
 'Share of inhabitants with at least 5 years of residence in %',
 'Amount of public transport stops within 500m, bus included',
 'Amount of restaurants and cafés within 500m (exc. fast food)',
 'Amount of cultural institutions within 500m (museums, cinemas, theaters, etc.)',
 'DROP Number of ngos, social and community centers, etc.',
 'DROP of hospital, clinics, pharmacies, etc.',
 'DROP of fire station, police, post box, townhall, etc.',
 'Amount of extra-curriculum educational institutions within 500m (music and language schools)',
 'DROP of schools',
 'DROP of universities ',
 'DROP of kindergartens',
 'Amount of urban furniture (picnic tables, benches, bbq, water points, etc.) within 500m',
 'Amount of places for outdoor leisure (swimming pools, parks, playgrounds, etc.) within 500m',
 'Amount of bars, pubs, nightclubs, etc. within 500m',
 'DROP Amount of lakes, rivers, etc.',
 'Share of houses built before 1940 in % (as of 2015)',
 'Share of houses built between 1941 and 1991 in % (as of 2015)',
 'Share of houses built between 1991 and 2001 in % (as of 2015)',
 'Vegetation volume in m3/m2',
 'Amount of other types of schools',
 'Amount of vocational schools',
 'Amount of primary schools',
 'Amount of Gymnasiums',
 'Amount of other secondary schools',
 'Amount of private schools',
 'Amount of schools for children with special needs',
 'Amount of kindergartens ',
 'Amount of rail / U-bahn / S-bahn and tram stations'))

st.write(f"{option} in each planning area")

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
