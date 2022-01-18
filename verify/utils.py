import json
import pprint

import requests

url = "https://stationapi.veriff.com/v1/sessions/"


def create_session(request_data):
    print(request_data)
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
    'X-AUTH-CLIENT': '0478fb5a-7aa2-4b52-b34d-b12a28f8a752',
    'Content-Type': 'application/json'
    }

    response = requests.request('POST', url, data=payload, headers=headers)
    pprint.pprint(response.json())

    # result, message, data = False, "Failed", None
    # try:
    #     # user.set_password(request_data.get("password"))
    #     user = user.save()
    #     # send user contact OTP
    #     result, message, data = True, "User created successfully", None
    # except Exception as e:
    #     result, message, data = False, str(e), None
    return True, "success", response
