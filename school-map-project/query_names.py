
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
query_keys = [public_transport, eating, night_life, culture, community, health_care, public_service, education, schools, universities, kindergarten, outdoor_facilities, outdoor_leisure, water]
