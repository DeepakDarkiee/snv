import json
import pprint

import requests
from decouple import config
from django.conf import settings

from .encoding import encode_to_base64
from .x_hmac import generate_signature

BASE_ENDPOINT = "https://stationapi.veriff.com/v1"


class Variff:
    @staticmethod
    def create_session_api(request_data):
        url = f"{BASE_ENDPOINT}/sessions/"
        firstName = request_data["firstName"]
        lastName = request_data["lastName"]
        idNumber = request_data["idNumber"]
        number = request_data["number"]
        country = request_data["country"]
        documentType = request_data["type"]
        vendorData = request_data["vendorData"]
        timestamp = request_data["timestamp"]

        person = {"firstName": firstName, "lastName": lastName, "idNumber": idNumber}
        document = {"number": number, "type": documentType, "country": country}

        verification = {
            "callback": "https://veriff.com",
            "vendorData": vendorData,
            "features": ["selfid"],
            "timestamp": timestamp,
            "person": person,
            "document": document,
        }

        session = {"verification": verification}

        payload = json.dumps(session)

        headers = {
            "X-AUTH-CLIENT": config("API_KEY"),  # api key
            "Content-Type": "application/json",
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        # pprint.pprint(response.json())
        session_object = response.json()
        return session_object

    @staticmethod
    def submit_session_api(session_id):
        key = config("API_SECRET_KEY")
        url = f"{BASE_ENDPOINT}/sessions/{session_id}"

        verification = {"status": "submitted", "timestamp": "2019-10-29T06:30:25.597Z"}
        session = {"verification": verification}
        payload = json.dumps(session)
        signature = generate_signature(payload, key)
        print(payload)
        headers = {
            "X-AUTH-CLIENT": config("API_KEY"),
            "X-HMAC-SIGNATURE": signature,
            "Content-Type": "application/json",
        }
        response = requests.request("PATCH", url, data=payload, headers=headers)
        return response

    @staticmethod
    def upload_document_front_api(request_data):
        key = config("API_SECRET_KEY")
        url = f"{BASE_ENDPOINT}/sessions/acc2e105-7956-4b9a-96b2-cc21ead5b14a/media"
        context = request_data["context"]
        content = request_data["content"]
        timestamp = request_data["timestamp"]
        inflowFeedback = True
        content = encode_to_base64(content)
        image = {
            "context": context,
            "content": content,
            "timestamp": timestamp,
            "inflowFeedback": inflowFeedback,
        }
        document = {"image": image}
        payload = json.dumps(document)
        print(payload)
        signature = generate_signature(payload, key)
        headers = {
            "X-AUTH-CLIENT": config("API_KEY"),
            "X-HMAC-SIGNATURE": signature,
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        pprint.pprint(response.json())
        document_front_object = response.json()
        return document_front_object

    @staticmethod
    def upload_document_back_api(request_data):
        key = config("API_SECRET_KEY")
        url = f"{BASE_ENDPOINT}/sessions/acc2e105-7956-4b9a-96b2-cc21ead5b14a/media"
        context = request_data["context"]
        content = request_data["content"]
        timestamp = request_data["timestamp"]
        inflowFeedback = True
        content = encode_to_base64(content)
        image = {
            "context": context,
            "content": content,
            "timestamp": timestamp,
            "inflowFeedback": inflowFeedback,
        }
        document = {"image": image}
        payload = json.dumps(document)
        signature = generate_signature(payload, key)
        print(payload)
        headers = {
            "X-AUTH-CLIENT": config("API_KEY"),
            "X-HMAC-SIGNATURE": signature,
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        pprint.pprint(response.json())
        document_back_object = response.json()
        return document_back_object

    @staticmethod
    def person_face_api(request_data):
        key = (config("API_SECRET_KEY"),)
        url = f"{BASE_ENDPOINT}/sessions/acc2e105-7956-4b9a-96b2-cc21ead5b14a/media"
        context = request_data["context"]
        content = request_data["content"]
        timestamp = request_data["timestamp"]
        inflowFeedback = True
        content = encode_to_base64(content)
        image = {
            "context": context,
            "content": content,
            "timestamp": timestamp,
            "inflowFeedback": inflowFeedback,
        }
        document = {"image": image}
        payload = json.dumps(document)
        signature = generate_signature(payload, key)
        print(payload)
        headers = {
            "X-AUTH-CLIENT": config("API_KEY"),
            "X-HMAC-SIGNATURE": signature,
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        pprint.pprint(response.json())
        person_face_object = response.json()
        Variff.submit_session_api("acc2e105-7956-4b9a-96b2-cc21ead5b14a")
        return person_face_object
