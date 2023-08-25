import requests
from requests.auth import HTTPBasicAuth
import yaml
from decouple import config


username = config('USERNAME1')
password = config('PASSWORD')

updated_data = {
  "asset": {
    "id": "bf7a7555-a8f8-4595-8721-b6719a44867a",
    "resourceType": "Asset",
    "name": "ds-template"
  },
  "value": "",
  "type": {
    "id": "00000000-0000-0000-0000-000000003116",
    "resourceType": "Attribute",
    "name": "TestAtt"
  },
  "system": False,
  "lastModifiedOn": 1476703764163,
  "createdBy": "4d250cc5-e583-4640-9874-b93d82c7a6cb",
  "lastModifiedBy": "a073ff90-e7bc-4b35-ba90-c4d475f642fe",
  "createdOn": 1475503010320,
  "id": "1329ff67-091a-492d-a531-b8631d1556d5"

}


url = f"https://adidas-dev.collibra.com/rest/2.0/attributes"
header = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=updated_data, auth=HTTPBasicAuth(username, password), headers=header)

# Check the response status code
if response.status_code == 201:
    data = response.json()
    print("POST request successful!")
    print(data)
else:
    print(f"POST request failed with status code {response.status_code}.")
    print(response.text)



def create_contract_asset (username, password, data):
    
    url = f"https://adidas-dev.collibra.com/rest/2.0/assets"
    header = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=data, auth=HTTPBasicAuth(username, password), headers=header)

    if response.status_code == 201:
        data = response.json()
        return data
    else:
        print(f"POST request failed with status code {response.status_code}.")
        print(response.text)
        return None