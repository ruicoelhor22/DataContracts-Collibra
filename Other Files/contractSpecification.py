import requests
from requests.auth import HTTPBasicAuth
import datetime
import yaml
from decouple import config


username = config('USERNAME1')
password = config('PASSWORD')

#DP (represents)schema: 00000000-0000-0000-0000-000000007038
# schema (contains)tables: 00000000-0000-0000-0000-000000007043
#table (is source for) table: 362efbbd-f0f1-4d65-8bd6-00fc19f87d32

header = {
    "Content-Type" : "application/json"
}
#---------------------
provider = input("Insert the name of the provider Data Product: ")
urlProviderInfo = f"https://adidas-dev.collibra.com/rest/2.0/assets?offset=0&limit=0&countLimit=-1&name={provider}&nameMatchMode=ANYWHERE&typeInheritance=true&excludeMeta=true&sortField=NAME&sortOrder=ASC"
responseProviderInfo = requests.get(urlProviderInfo, auth=HTTPBasicAuth(username, password), headers=header)

dataProviderInfo = responseProviderInfo.json()
resultsProviderInfo = dataProviderInfo.get("results", [])
if resultsProviderInfo:
    first_assetP = resultsProviderInfo[0]    
else:
    print("No assets found in the response.")
#-------------------

#-------------------
consumer = input("Insert the name of the consumer Data Product: ")
urlConsumerInfo = f"https://adidas-dev.collibra.com/rest/2.0/assets?offset=0&limit=0&countLimit=-1&name={consumer}&nameMatchMode=ANYWHERE&typeInheritance=true&excludeMeta=true&sortField=NAME&sortOrder=ASC"
responseConsumerInfo = requests.get(urlConsumerInfo, auth=HTTPBasicAuth(username, password), headers=header)

dataConsumerInfo = responseConsumerInfo.json()
resultsConsumerInfo = dataConsumerInfo.get("results", [])
if resultsConsumerInfo:
    first_assetC = resultsConsumerInfo[0]    
else:
    print("No assets found in the response.")
#------------------

userP = first_assetP.get("createdBy", "N/A")
userC = first_assetC.get("createdBy", "N/A")

# Fetch user information for first_assetP
urlUserP = f"https://adidas-dev.collibra.com/rest/2.0/users/{userP}"
responseUserP = requests.get(urlUserP, auth=HTTPBasicAuth(username, password), headers=header)
dataUserP = responseUserP.json()
resultsUserP = dataUserP.get("results", [])
if resultsUserP:
    userInfoP = resultsUserP[0]
    # Process userInfoP if needed
    print(first_assetP)
else:
    #print("No assets found for first_assetP in the response.")
        print( )

# Fetch user information for first_assetC
urlUserC = f"https://adidas-dev.collibra.com/rest/2.0/users/{userC}"
responseUserC = requests.get(urlUserC, auth=HTTPBasicAuth(username, password), headers=header)
dataUserC = responseUserC.json()
resultsUserC = dataUserC.get("results", [])
if resultsUserC:
    userInfoC = resultsUserC[0]
    # Process userInfoC if needed
else:
    #print("No assets found for first_assetC in the response.")
    print( )
    


# Check the response status code
if responseProviderInfo.status_code == 200 and responseConsumerInfo.status_code == 200 and responseUserP.status_code == 200 and responseUserC.status_code == 200:
    
    print("Data Contract Specification: 0.0.1")
    print("INFO")
    print("     ID: ")
    print("     Purpose: ") #filled in by the person that wants to consume the data product
    print("     Status: ")
    print("     StartDate: ")
    print("     EndDate: ")

    print("PROVIDER")
    print("     Creator ID: ", first_assetP.get("createdBy", "N/A"))
    creationDate = datetime.datetime.fromtimestamp(first_assetP.get("createdOn") / 1000)
    print("     Created on: ", creationDate)
    first_name = dataUserP['firstName']
    last_name = dataUserP['lastName']
    print("     Creator Name: ", first_name + ' ' + last_name)
    print("     DataProduct ID: ", first_assetP.get("id", "N/A"))
    print("     DataProduct Name: ", first_assetP.get("displayName", "N/A"))
    print("     Output Port Name: ") 
    print("     Output Port ID: ")
    
    print("CONSUMER")
    print("     Creator ID: ", first_assetC.get("createdBy", "N/A"))
    creationDate = datetime.datetime.fromtimestamp(first_assetC.get("createdOn") / 1000)
    print("     Created on: ", creationDate)
    first_name = dataUserC['firstName']
    last_name = dataUserC['lastName']
    print("     Creator Name: ", first_name + ' ' + last_name)
    print("     DataProduct ID: ", first_assetC.get("id", "N/A"))
    print("     DataProduct Name: ", first_assetC.get("displayName", "N/A"))
    print("     Output Port Name: ")
    print("     Output Port ID: ")
    
    print("TERMS")
    print("     Usage: ")
    print("     Limitations: ")
    print("     Billing:")
    print("     NoticePeriod: ")
    
    # Data for Provider and Consumer
    provider_data = {
        'Creator ID': first_assetP.get("createdBy", "N/A"),
        'Created on': datetime.datetime.fromtimestamp(first_assetP.get("createdOn") / 1000).strftime('%Y-%m-%d %H:%M:%S'),
        'Creator Name': f"{dataUserP['firstName']} {dataUserP['lastName']}",
        'DataProduct ID': first_assetP.get("id", "N/A"),
        'DataProduct Name': first_assetP.get("displayName", "N/A"),
        'Output Port Name': "",
        'Output Port ID': "",
    }

    consumer_data = {
        'Creator ID': first_assetC.get("createdBy", "N/A"),
        'Created on': datetime.datetime.fromtimestamp(first_assetC.get("createdOn") / 1000).strftime('%Y-%m-%d %H:%M:%S'),
        'Creator Name': f"{dataUserC['firstName']} {dataUserC['lastName']}",
        'DataProduct ID': first_assetC.get("id", "N/A"),
        'DataProduct Name': first_assetC.get("displayName", "N/A"),
        'Output Port Name': "",
        'Output Port ID': "",
    }

    # Data Contract Specification
    data_contract_spec = {
        'Data Contract Specification': '0.0.1',
        'INFO': {
            'ID': "",
            'Purpose': "",
            'Status': "",
            'StartDate': "",
            'EndDate': "",
        },
        'PROVIDER': provider_data,
        'CONSUMER': consumer_data,
        'TERMS': {
            'Usage': "",
            'Limitations': "",
            'Billing': "",
            'NoticePeriod': "",
        }
    }

    # Reorder the keys to order
    ordered_data_contract_spec = {
        'Data Contract Specification': data_contract_spec['Data Contract Specification'],
        'INFO': data_contract_spec['INFO'],
        'PROVIDER': data_contract_spec['PROVIDER'],
        'CONSUMER': data_contract_spec['CONSUMER'],
        'TERMS': data_contract_spec['TERMS'],
    }
    # File path where to save the YAML data
    file_path = 'data_contract_spec.yaml'

    # Write the data to the YAML file
    with open(file_path, 'w') as yaml_file:
        yaml.dump(data_contract_spec, yaml_file)

    print(f"Data has been written to '{file_path}' successfully.")


else:
    print(f"GET Provider Info request failed with status code {responseProviderInfo.status_code}.")
    print(responseProviderInfo.text)
    print(f"GET Consumer Info request failed with status code {responseConsumerInfo.status_code}.")
    print(responseConsumerInfo.text)


