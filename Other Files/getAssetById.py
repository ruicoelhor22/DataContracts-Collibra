import requests
from requests.auth import HTTPBasicAuth
from decouple import config


username = config('USERNAME1')
password = config('PASSWORD')
header = {
    "Content-Type" : "application/json"
}
#url = "https://adidas-dev.collibra.com/rest/2.0/assets/614fd946-767d-4984-9735-a9f013a4510e"
#url = "https://adidas-dev.collibra.com/rest/2.0/assets?offset=0&limit=0&countLimit=-1&name=ds-template&nameMatchMode=ANYWHERE&typeInheritance=true&excludeMeta=true&sortField=NAME&sortOrder=ASC"
#url = "https://adidas-dev.collibra.com/rest/2.0/relations?offset=0&limit=0&countLimit=-1&relationTypeId=362efbbd-f0f1-4d65-8bd6-00fc19f87d32&sourceTargetLogicalOperator=AND"
url = "https://adidas-dev.collibra.com/rest/2.0/relations?offset=0&limit=0&countLimit=-1&relationTypeId=362efbbd-f0f1-4d65-8bd6-00fc19f87d32&sourceId=3f7e22f8-f89e-43c8-8891-69cfb1e50b34&sourceTargetLogicalOperator=AND"

response = requests.get(url, auth=HTTPBasicAuth(username, password), headers=header)

if response.status_code == 200:
    data = response.json()
    print(data)
    """
    
    for result in data["results"]:
        source_id = result["source"]["id"]
        target_id = result["target"]["id"]
        print("Source ID:", source_id)
        print("Target ID:", target_id)
    
    results = data.get("results", [])
    
    if results:
        first_asset = results[0]
        created_by = first_asset.get("createdBy")
        
        if created_by:
            print("GET request successful!")
            print("Creatir ID: ", created_by)
        else:
            print("Creator ID: information not found for the specific asset.")
    else:
        print("No assets found in the response.")
    """   
else:
    print("Failed to retrieve data from the API.")







"""
# Check the response status code
if response.status_code == 200:
    data = response.json()
    print("GET request successful!")
    print("Created By: ", data[0]["createdBy"])
    print("ID:", data["id"])
else:
    print(f"GET request failed with status code {response.status_code}.")
    print(response.text)


#print("Info: " , response.json())
"""