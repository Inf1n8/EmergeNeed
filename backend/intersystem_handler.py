import uuid
import requests
from config import (PATIENT_ENDPOINT, INTERSYSTEM_API_URL, INTERSYSTEM_API_KEY)

def get_random_id():
    return uuid.uuid4()

def intersystem_post_request_handler(endpoint, payload):
    headers = {
                'x-api-key': INTERSYSTEM_API_KEY
            }
    response = requests.request("POST", INTERSYSTEM_API_URL+endpoint, headers=headers, data=payload)
    return response

def create_patient_record(data):
    data['name'] = [
    {
      "use": "official",
      "family": data.get('lastname'),
      "given": [
        data.get('firstname')
      ]
    }
    ]
    del data['firstname']
    del data['lastname']
    data = {**data, 'id': get_random_id(), 'resourceType': 'Patient'}
    res = intersystem_post_request_handler(PATIENT_ENDPOINT, data)
    return res
    
