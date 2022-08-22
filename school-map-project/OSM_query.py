from http.client import SWITCHING_PROTOCOLS
from textwrap import indent
import requests
from query_names import public_transport, outdoor_leisure
import json


""" Functions to send request to OSM's API """

overpass_url = "http://overpass-api.de/api/interpreter"


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

    #print(query_params_osm(location = "Berlin",
                    #keys = public_transport))
    #print(dict(public_transport))
    print(query_params_osm('Berlin', outdoor_leisure, limit=''))
