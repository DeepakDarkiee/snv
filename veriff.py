import requests
import pprint
import json

url = 'https://stationapi.veriff.com/v1/sessions/'

payload = json.dumps({
    'verification': {
        'callback': 'https://veriff.com',
        'person': {
          'firstName': 'John',
          'lastName': 'Smith',
          # 'idNumber': '123456789'
        },
        'document': {
          'number': 'B01234567',
          'type': 'PASSPORT',
          'country': 'EE'
        },
        'vendorData': '11111111',
        'features': [
          'selfid'
        ],
        'timestamp': '2016-05-19T08:30:25.597Z'
    }
})

headers = {
    'X-AUTH-CLIENT': '0478fb5a-7aa2-4b52-b34d-b12a28f8a752',
    'Content-Type': 'application/json'
}

response = requests.request('POST', url, data=payload, headers=headers)
pprint.pprint(response.json())