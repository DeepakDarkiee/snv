import json
import pprint

import requests

url = "https://stationapi.veriff.com/v1/sessions/"


class Variff:
    @staticmethod
    def create_session_api(request_data):
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
            "X-AUTH-CLIENT": "0478fb5a-7aa2-4b52-b34d-b12a28f8a752",  # api key
            "Content-Type": "application/json",
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        # pprint.pprint(response.json())
        session_object = response.json()
        return session_object
