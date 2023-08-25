import requests
from requests.auth import HTTPBasicAuth
import yaml
from decouple import config


username = config('USERNAME1')
password = config('PASSWORD')
'''
def read_yaml(file_path) :
    with open (file_path, 'r') as file:
        data =yaml.safe_load(file)
    return data
if __name__ == "__main__" :
    file_path = input("Enter the file path: ")
    try:
        yaml_data = read_yaml(file_path)
        print("Successfully read YAML file:")
        print(yaml_data)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse YAML file. {e}")
'''
updated_data = {
  "sourceId" : "f26918ea-a4cb-41da-a5da-2b2bfc2efc04",
  "targetId" : "ef1554b4-564e-4c08-981e-5ba7dc5d046f",
  "typeId" : "2f6ccb30-25d9-4681-b31b-ba7619729dde"

}


url = f"https://adidas-dev.collibra.com/rest/2.0/relations"
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