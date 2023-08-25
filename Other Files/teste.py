import sys
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


counter = 0

ref = requests.get
'''
def get(*argsv,**argsm):
    global counter
    counter += 1
    print(counter)
    return ref(*argsv,**argsm)

requests.get = get
'''

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
    print("No assets found in the response.1")
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
    print("No assets found in the response.2")


userP = first_assetP.get("createdBy", "N/A")
userC = first_assetC.get("createdBy", "N/A")
#------------------


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
#--------------        

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
#-----------------


#function to get the target when provided the source
def get_first_asset(source_asset_Id, username, password, header):
    url = f"https://adidas-dev.collibra.com/rest/2.0/relations?offset=0&limit=0&countLimit=-1&sourceId={source_asset_Id}&sourceTargetLogicalOperator=AND"
    response = requests.get(url, auth=HTTPBasicAuth(username, password), headers=header)
    data = response.json()
    results = data.get("results", [])
    if results:
        return results
    else:
        #print("No assets found in the response.3")
        #sys.exit("Execution stopped due to a certain condition.")
        return None
#-------------

    #function to see if the given source id has a relation of type : if source for
def print_url_response(asset_id, username, password, header):
    url = f"https://adidas-dev.collibra.com/rest/2.0/relations?offset=0&limit=0&countLimit=-1&relationTypeId=362efbbd-f0f1-4d65-8bd6-00fc19f87d32&sourceId={asset_id}&sourceTargetLogicalOperator=AND"
    response = requests.get(url, auth=HTTPBasicAuth(username, password), headers=header)
    data = response.json()
    results = data.get("results", [])
    if results:
        for result in results:
            target_id = result.get("source", {}).get("id", "N/A")
            target_name = result.get("source", {}).get("name", "N/A")
            print("     Output Port ID: " + target_id)
            print("     Output Port Name: " + target_name)
        return True
    else:
        return False
#-------------------
    

# Check the response status code
if responseProviderInfo.status_code == 200 and responseConsumerInfo.status_code == 200 and responseUserP.status_code == 200 and responseUserC.status_code == 200:
    
    print("Data Contract Specification: 0.0.1")
    print("INFO")
    print("     ID: ")
    print("     Purpose: ")
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
    print("     Input Port ID: ")
    print("     Input Port Name: ")
    #iteration through get_first_asset and verification if the given ID has a relation of type: if source for
    source_asset_Id = first_assetP.get("id", "N/A")
    first_asset = get_first_asset(source_asset_Id, username, password, header)
    isTrue = False
    no_assets_found_message_printed = False
    while not isTrue:
        if first_asset is not None:
            for asset in first_asset:
                asset_id = asset.get("target", {}).get("id", "N/A")
                isTrue = print_url_response(asset_id, username, password, header)
                if  not isTrue:  
                    first_asset = get_first_asset(asset_id, username, password, header)
            no_assets_found_message_printed = False  # Reset the flag since assets are found
        else:
            if not no_assets_found_message_printed:
                #print("No assets found in the response.")
                print("     Output Port ID: ")
                print("     Output Port Name: ")
                no_assets_found_message_printed = True  # Set the flag to indicate the message was printed
            break
    #-------------------
    
    
    print("CONSUMER")
    print("     Creator ID: ", first_assetC.get("createdBy", "N/A"))
    creationDate = datetime.datetime.fromtimestamp(first_assetC.get("createdOn") / 1000)
    print("     Created on: ", creationDate)
    first_name = dataUserC['firstName']
    last_name = dataUserC['lastName']
    print("     Creator Name: ", first_name + ' ' + last_name)
    print("     DataProduct ID: ", first_assetC.get("id", "N/A"))
    print("     DataProduct Name: ", first_assetC.get("displayName", "N/A"))
    #iteration through get_first_asset and verification if the given ID has a relation of type: if source for
    '''
    aa = first_assetC.get("id", "N/A")
    second_asset = get_first_asset(aa, username, password, header)
    isTrue = False
    while isTrue == False:
        if first_asset is not None:
            for asset in second_asset:
                asset_id = asset.get("target", {}).get("id", "N/A")
                isTrue = print_url_response(asset_id, username, password, header)
                if  isTrue == False:  
                    seconde_asset = get_first_asset(asset_id, username, password, header)
        else:
            print("     Output Port ID: This asset doesn't have an Output Port.")
            #break
            pass  
    '''      
    print("     Output Port ID: ")
    print("     Output Port Name: ")
    
    
    print("TERMS")
    print("     Usage: ")
    print("     Limitations: ")
    print("     Billing:")
    print("     NoticePeriod: ")
    
    

    
    
    
    '''
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
    '''

else:
    print(f"GET Provider Info request failed with status code {responseProviderInfo.status_code}.")
    print(responseProviderInfo.text)
    print(f"GET Consumer Info request failed with status code {responseConsumerInfo.status_code}.")
    print(responseConsumerInfo.text)


