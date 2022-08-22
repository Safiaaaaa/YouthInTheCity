import pandas as pd
from query_names import public_transport, eating, night_life, culture, community, education, health_care, public_service
from query_names import schools, universities, kindergarten, outdoor_facilities, asylum, outdoor_leisure, water
from OSM_query import query_params_osm

def get_public_transp(location):
    #for querie in public_transport:
    new_querie = query_params_osm(location = location, keys = public_transport, features = 'nodes')
    df_public_transport = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
    df_public_transport['coor'] = list(zip(df_public_transport.lat, df_public_transport.lon))
    df_public_transport.to_csv('data/api_features/transport.csv', index=False)
    return df_public_transport

def get_eating(location):
    new_querie = query_params_osm(location = location, keys = eating, features = 'nodes')
    df_eating = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
    df_eating['coor'] = list(zip(df_eating.lat, df_eating.lon))
    df_eating.to_csv('data/api_features/eating.csv', index=False)
    return df_eating

def get_night_life(location):
    new_querie = query_params_osm(location = location, keys = night_life, features = 'nodes')
    df_night_life = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
    df_night_life['coor'] = list(zip(df_night_life.lat, df_night_life.lon))
    df_night_life.to_csv('data/api_features/night.csv', index=False)
    return df_night_life

def get_culture(location):
    new_querie = query_params_osm(location = location, keys = culture, features = 'nodes')
    df_culture = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
    df_culture['coor'] = list(zip(df_culture.lat, df_culture.lon))
    df_culture.to_csv('data/api_features/culture.csv', index=False)
    return df_culture

def get_community(location):
    new_querie = query_params_osm(location = location, keys = community, features = 'nodes')
    df_community = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
    df_community['coor'] = list(zip(df_community.lat, df_community.lon))
    df_community.to_csv('data/api_features/community.csv', index=False)
    return df_community

def get_health_care(location):
    new_querie = query_params_osm(location = location, keys = health_care, features = 'nodes')
    df_health_care = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
    df_health_care['coor'] = list(zip(df_health_care.lat, df_health_care.lon))
    df_health_care.to_csv('data/api_features/health_care.csv', index=False)
    return df_health_care

def get_public_service(location):
    new_querie = query_params_osm(location = location, keys = public_service, features = 'nodes')
    df_public_service = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
    df_public_service['coor'] = list(zip(df_public_service.lat, df_public_service.lon))
    df_public_service.to_csv('data/api_features/pub_serv.csv', index=False)
    return df_public_service

def get_education(location):
    new_querie = query_params_osm(location = location, keys = education, features = 'nodes')
    df_education = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
    df_education['coor'] = list(zip(df_education.lat, df_education.lon))
    df_education.to_csv('data/api_features/education.csv', index=False)
    return df_education

def get_schools(location):
    new_querie = query_params_osm(location = location, keys = schools, features = 'nodes')
    df_schools = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
    df_schools['coor'] = list(zip(df_schools.lat, df_schools.lon))
    df_schools.to_csv('data/api_features/schools.csv', index=False)
    return df_schools

def get_universities(location):
    new_querie = query_params_osm(location = location, keys = universities, features = 'nodes')
    df_universities = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
    df_universities['coor'] = list(zip(df_universities.lat, df_universities.lon))
    df_universities.to_csv('data/api_features/schools.csv', index=False)
    return df_universities

def get_kindergarten(location):
    new_querie = query_params_osm(location = location, keys = kindergarten, features = 'nodes')
    df_kindergarten = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
    df_kindergarten['coor'] = list(zip(df_kindergarten.lat, df_kindergarten.lon))
    df_kindergarten.to_csv('data/api_features/kindergarten.csv', index=False)
    return df_kindergarten

def get_outdoor_facilities(location):
    #for querie in outdoor_facilities:
    new_querie = query_params_osm(location = location, keys = outdoor_facilities, features = 'nodes')
    df_outdoor_facilities = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
    df_outdoor_facilities['coor'] = list(zip(df_outdoor_facilities.lat, df_outdoor_facilities.lon))
    df_outdoor_facilities.to_csv('data/api_features/out_facilities.csv', index=False)
    return df_outdoor_facilities

def get_outdoor_leisure(location):
    new_querie = query_params_osm(location = location, keys = outdoor_leisure, features = 'nodes')
    df_outdoor_leisure = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
    df_outdoor_leisure['coor'] = list(zip(df_outdoor_leisure.lat, df_outdoor_leisure.lon))
    df_outdoor_leisure.to_csv('data/api_features/out_leisure,.csv', index=False)
    return df_outdoor_leisure

def get_water(location):
    new_querie = query_params_osm(location = location, keys = water, features = 'nodes')
    df_water = pd.DataFrame(new_querie['elements'])[['lat', 'lon']]
    df_water['coor'] = list(zip(df_water.lat, df_water.lon))
    df_water.to_csv('data/api_features/water.csv', index=False)
    return df_water


def get_all(location):

    # return get_public_transp(location = location)
    get_public_transp(location = location)
    get_eating(location = location)
    get_night_life(location = location)
    get_culture(location = location)
    get_community(location = location)
    get_health_care(location = location)
    get_public_service(location = location)
    get_education(location = location)
    get_schools(location = location)
    get_universities(location = location)
    get_kindergarten(location = location)
    get_outdoor_facilities(location=location)
    get_outdoor_leisure(location=location)
    get_water(location = location)


if __name__ == "__main__":
    print(get_community('Berlin'))
