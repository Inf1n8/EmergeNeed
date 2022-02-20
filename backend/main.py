import os
from flask import Flask, request
from flask_restful import Resource, Api
import google.cloud.dialogflow_v2 as dialogflow

from ner import get_entities
from config import (DIALOGFLOW_PROJECT_ID, SESSION_ID)
from rec_hospitals import get_hospital_recommendations
from intersystem_handler import create_patient_record

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './hospitalhoppers-6c9e1bacd23a.json'

app = Flask(__name__)
api = Api(app)

session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

class IntentRecognition(Resource):
    def post(self):
        body = request.get_json()
        if body.get('text') is None:
            {'message': 'BAD_REQUEST', 'error_message': 'Missing text parameter in the body'}, 400
        res = get_entities(body.get('text'), session_client, session)
        return res, 200

class HospitalList(Resource):
    def post(self):
        payload = request.get_json()
        res = get_hospital_recommendations(payload)
        return res, 200

class Patient(Resource):
    def post(self):
        payload = request.get_json()
        res = create_patient_record(payload)
        return res.json()


api.add_resource(IntentRecognition, '/intent')
api.add_resource(HospitalList, '/hospitals')
api.add_resource(Patient, '/patient')

if __name__ == '__main__':
    app.run(debug=True)