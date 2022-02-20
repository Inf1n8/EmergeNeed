import requests
import geopy.distance
from config import (API_KEY, TEXT_SEARCH_API)

def google_maps_api_request_handler(endpoint, params):
    params['key'] = API_KEY
    req = requests.get(endpoint, params=params)
    status_code, data = req.status_code, req.json()
    return status_code, data

def get_distance(res, lat, lon):
    for i in res:
        coords_1 = (lat, lon)
        coords_2 = (i['geometry']['location']['lat'], i['geometry']['location']['lng'])
        i['distance'] = geopy.distance.geodesic(coords_1, coords_2).mi
        i['number_of_available_beds'] = 20
        i['occupancy_rate'] = '38%'
    return res

def get_hospital_recommendations(data):
    query = f"{','.join(data.get('symptoms', []))} hospitals"
    location = f"{data.get('lat')},{data.get('lon')}"
    status_code, res = google_maps_api_request_handler(TEXT_SEARCH_API, {'query': query, 'location': location})
    res = get_distance(res['results'], data.get('lat'), data.get('lon'))
    return res