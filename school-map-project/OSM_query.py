from http.client import SWITCHING_PROTOCOLS
import requests


""" API's URL """

overpass_url = "http://overpass-api.de/api/interpreter"


""" OSM query keys (per feature) """


public_transport = {'amenity':['bus_station'],
                   'highway':['bus_stop','platform'],
                   'public_transport':['stop_position','platform','station','stop_area'],
                   'railway':['station','tram_stop', 'subway_entrance']}

eating = {'amenity':['cafe','restaurant', 'food_court', 'ice_cream']}

night_life = { 'amenity':['bar','pub','biergarten', 'nightclub', 'swingerclub',
            'casino']}

culture = {'amenity':['theatre','public_bookcase', 'events_venue',
        'cinema','arts_centre', 'museum', 'cultural_center', 'gallery',
        'events_venue', 'planetarium']}

community = {'amenity': ['social_centre','community_centre', 'association',
        'charity', 'ngo']}

education = {'amenity': ['educational_institution', 'language_school',
        'music_school']}

health_care = {'amenity':['baby_hatch','clinic','dentist', 'doctors', 'hospital',
            'nursing_home', 'pharmacy','social_facility','veterinary']}

public_service = {'amenity':['courthouse','fire_station','police',
                      'post_box', 'post_office', 'townhall']}

schools = {'amenity':['school', 'gymnasium', 'Grundschule', 'Schule']}

universities = {'amenity':['college','university']}

kindergarten = {'amenity': ['kindergarten', 'childcare', 'preschool']}

outdoor_facilities = {'amenity':['bbq', 'bench', 'drinking_water', 'give_box','shelter',
            'telephone', 'water_point'],
            'leisure':['bandstand', 'picnic_table']}

asylum = {'amenity': ['refugee_site']}

outdoor_leisure = {'leisure':['swimming_pool', 'park','playground','garden','swimming_area']}

water = {'natural':['water','beach', 'lake', 'river', 'shore'],
         'amenity':['fountain']}

columns = ['query_string','name','distance','geomtype','jsontype','shapelytype','category']
columns_wb = ['query_string', 'name','distance','geomtype','jsontype','shapelytype','category','whitefilter','blackfilter']

def param_nodes(keys):
    '''converts the dict into a string, returns a str'''
    osm_keys = ''
    for k,val in keys.items():
        for v in val:
            osm_keys += f"""node['{k}'='{v}'](area.city);"""
    return osm_keys


def query_params_osm(location, keys, limit=''):
    '''Adding keys and values as a dictionary, example: keys_values_osm = {'amenity':['bbq','cafe']}
    several values can be added to a same key as a list, returns a dict
    feat = nodes, ways or areas (geometry type) - here only nodes
    limit = number (optional query limit)'''
    location_area = f'area[name="{location}"]->.city'

    params = param_nodes(dict(keys))
    out_type = 'center'

    overpass_query = f"""
                    [out:json][timeout:900];
                    {location_area};
                    ({params}
                    );
                    (._;>;);
                    out {limit} {out_type};
                    """

    response = requests.get(overpass_url,
                            params={'data': overpass_query})
    return response.json()

if __name__ == "__main__":
# print(param_nodes(keys = {'amenity': ['atm', 'bank', 'bureau_de_change']}))

    print(query_params_osm(location = "Berlin",
                    keys = schools))
