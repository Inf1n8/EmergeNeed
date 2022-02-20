import uuid
import requests
from datetime import datetime
from config import (
    PATIENT_ENDPOINT, 
    INTERSYSTEM_API_URL, 
    INTERSYSTEM_API_KEY, 
    QUESTIONNAIRE_ENDPOINT, 
    GOAL_ENDPOINT, 
    QUESTIONNAIRE_RESPONSE_ENDPOINT,
    IMMUNIZATION_ENDPOINT,
    APPOINTMENT_ENDPOINT
)

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
    
def create_questionnaire_response(data):
    data = {**data, 'language': 'english-US', 'authored': str(datetime.now()), 'resourceType': 'QuestionnaireResponse', 
    'id': get_random_id(),
    "author": {
        "reference": "http://hl7.org/fhir/Practitioner/example",
        "type": "Practitioner"
    },  "subject": {
    "reference": "http://hl7.org/fhir/Patient/1",
    "type": "Patient"
    }}
    res = intersystem_post_request_handler(QUESTIONNAIRE_RESPONSE_ENDPOINT, data)
    return res

def create_goal(data):
    data = {**data, 'language': 'english-US', 'resourceType': 'Goal', 'id': get_random_id(),  'note': [{
        'id': get_random_id(),
        'text': 'Feeling relaxed',
        'time': str(datetime.now()),
        'priority': {
            'id': get_random_id(),
            'description': 'high-priority'
        }
    }]}
    res = intersystem_post_request_handler(GOAL_ENDPOINT, data)
    return res

def create_questionnaire(data):
    data = {**data, 'language': 'english-US', 'date': str(datetime.now()), 'resourceType': 'Questionnaire', 
    'id': get_random_id(),
    'description': 'Wellness assessment',
    'item': [{
        'id': get_random_id(),
        'type': 'integer',
        'text': 'On a scale of 1-10, how do you feel today?'
    }],
    "publisher": "Dr. Henry",  "subject": {
    "reference": "http://hl7.org/fhir/Patient/1",
    "type": "Patient"
    }}
    res = intersystem_post_request_handler(QUESTIONNAIRE_ENDPOINT, data)
    return res


def create_immunization(data):
    data = {**data, 'id': get_random_id(), 'language': 'english-US',
    "resourceType": "Immunization", 
    'manufacturer': {
        'id': get_random_id(),
        'display': 'Pfizer'
    },
    "patient": {
    "reference": "http://hl7.org/fhir/Patient/1",
    "type": "Patient"
    }}
    res = intersystem_post_request_handler(IMMUNIZATION_ENDPOINT, data)
    return res


def create_appointment(data):
    data = {**data, 'id': get_random_id(), 'language': 'english-US',
    "resourceType": "Appointment",
    "priority": 5,
    "appointmentType": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/v2-0276",
        "code": "WALKIN",
        "display": "A previously unscheduled walk-in visit"
      }
    ]
  },
    'manufacturer': {
        'id': get_random_id(),
        'display': 'Pfizer'
    },
    "patient": {
    "reference": "http://hl7.org/fhir/Patient/1",
    "type": "Patient"
    }}
    res = intersystem_post_request_handler(APPOINTMENT_ENDPOINT, data)
    return res
