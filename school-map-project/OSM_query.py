from http.client import SWITCHING_PROTOCOLS
from textwrap import indent
import requests
from query_names import outdoor_leisure

""" Functions to send request to OSM's API """

overpass_url = "http://overpass-api.de/api/interpreter"

def param_nodes(keys):
    '''converts the dict into a string, returns a str'''
    osm_keys = ''
    for k,val in keys.items():
        for v in val:
            osm_keys += f"""node['{k}'='{v}'](area.city);"""
    return osm_keys

culture = {'amenity':['theatre','public_bookcase', 'events_venue',
        'cinema','arts_centre', 'museum', 'cultural_center', 'gallery',
        'events_venue', 'planetarium']}

def query_params_osm(location, keys, limit=''):
    '''Adding keys and values as a dictionary, example: keys_values_osm = {'amenity':['bbq','cafe']}
    several values can be added to a same key as a list, returns a dict
    feat = nodes, ways or areas (geometry type) - here only nodes
    limit = number (optional query limit)'''
    location_area = f'area[name="{location}"]->.city'

    params = param_nodes(keys)

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
    if response.status_code == 200:
        return response.json()
    else:
        return None




if __name__ == "__main__":

    print(query_params_osm('Berlin', outdoor_leisure, limit=''))
