from contextlib import contextmanager
import datetime
import requests
from requests.auth import HTTPBasicAuth
from decouple import config
import sys
import io
import time
import pytz



def get_data_contract_specification(username, password, provider, consumer):
    header = {
        "Content-Type": "application/json"
    }
    
    #function to get the target when provided the source
    def get_first_asset(source_asset_Id):
        url = f"https://adidas-dev.collibra.com/rest/2.0/relations?offset=0&limit=0&countLimit=-1&sourceId={source_asset_Id}&sourceTargetLogicalOperator=AND"
        response = requests.get(url, auth=HTTPBasicAuth(username, password), headers=header)
        data = response.json()
        results = data.get("results", [])
        if results:
            return results
        else:
            return None
    #-----------------
    
    #function to see if the given source id has a relation of type : if source for
    def print_url_response(asset_id):
        url = f"https://adidas-dev.collibra.com/rest/2.0/relations?offset=0&limit=0&countLimit=-1&relationTypeId=362efbbd-f0f1-4d65-8bd6-00fc19f87d32&sourceId={asset_id}&sourceTargetLogicalOperator=AND"
        response = requests.get(url, auth=HTTPBasicAuth(username, password), headers=header)
        data = response.json()
        results = data.get("results", [])
        if results:
            for result in results:
                target_id = result.get("source", {}).get("id", "N/A")
                target_name = result.get("source", {}).get("name", "N/A")
                print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Output Port ID: " + target_id)
                #print("     Output Port Name: " + target_name)
            return True
        else:
            return False
    #------------------


    #Function to create data contract asset
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
    #------------------

    #Function to create relationships
    def create_relation (username, password, data):
        url = f"https://adidas-dev.collibra.com/rest/2.0/relations"
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
    #------------------
    #Function to create resposibilites
    def create_responsibilities (username, password, data):
        url = f"https://adidas-dev.collibra.com/rest/2.0/responsibilities"
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
    #------------------

    #Function to update description attribute of an asset
    def update_contract_description (username, password, assetId, info):
        url = f"https://adidas-dev.collibra.com/rest/2.0/assets/{assetId}/attributes"
        header = {
            "Content-Type": "application/json"
        }
        data = {
            "typeId": "00000000-0000-0000-0000-000000003114",
            "values": [f"{info}"]
        }
        response = requests.put(url, json=data, auth=HTTPBasicAuth(username, password), headers=header)

        if response.status_code // 100 == 2:  
            data = response.json()
            return data
        else:
            print(f"PUT request failed with status code {response.status_code}.")
            print(response.text)
            return None
    #------------------

    # Function to update attributes of an asset
    def update_attributes(username, password, assetId, attributes):
        url = f"https://adidas-dev.collibra.com/rest/2.0/assets/{assetId}/attributes"
        header = {
            "Content-Type": "application/json"
        }

        updated_attributes = []

        for attr in attributes:
            data = {
                "typeId": attr["typeId"],
                "values": [attr["value"]]
            }
            response = requests.put(url, json=data, auth=HTTPBasicAuth(username, password), headers=header)

            if response.status_code // 100 == 2:
                updated_attributes.append(data)
            else:
                print(f"PUT request failed for attribute {attr['typeId']} with status code {response.status_code}.")
                print(response.text)
                return None
    #------------------

    #Function to capture the information that is printed to then use it elsewere
    def capture_stdout(func):
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        func()
        sys.stdout = old_stdout
        return new_stdout.getvalue()
    
    #------------------

    
    # Getting the Provider Info
    urlProviderInfo = f"https://adidas-dev.collibra.com/rest/2.0/assets?offset=0&limit=0&countLimit=-1&name={provider}&nameMatchMode=EXACT&typeInheritance=true&excludeMeta=true&sortField=NAME&sortOrder=ASC"
    responseProviderInfo = requests.get(urlProviderInfo, auth=HTTPBasicAuth(username, password), headers=header)
    dataProviderInfo = responseProviderInfo.json()
    resultsProviderInfo = dataProviderInfo.get("results", [])
    if resultsProviderInfo:
        first_assetP = resultsProviderInfo[0]
    else:
        print("No assets found in the response.1")
        return
    #----------------
    

    # Getting the Consumer Info
    urlConsumerInfo = f"https://adidas-dev.collibra.com/rest/2.0/assets?offset=0&limit=0&countLimit=-1&name={consumer}&nameMatchMode=EXACT&typeInheritance=true&excludeMeta=true&sortField=NAME&sortOrder=ASC"
    responseConsumerInfo = requests.get(urlConsumerInfo, auth=HTTPBasicAuth(username, password), headers=header)
    dataConsumerInfo = responseConsumerInfo.json()
    resultsConsumerInfo = dataConsumerInfo.get("results", [])
    if resultsConsumerInfo:
        first_assetC = resultsConsumerInfo[0]
    else:
        print("No assets found in the response.2")
        return
    #-----------------
    
    #-----------------
    userP = first_assetP.get("createdBy", "N/A")
    userC = first_assetC.get("createdBy", "N/A")
    #-----------------


    #-----------------
    urlUserP = f"https://adidas-dev.collibra.com/rest/2.0/users/{userP}"
    responseUserP = requests.get(urlUserP, auth=HTTPBasicAuth(username, password), headers=header)
    dataUserP = responseUserP.json()
    resultsUserP = dataUserP.get("results", [])
    if resultsUserP:
        userInfoP = resultsUserP[0]
        # Process userInfoP if needed
        print(first_assetP)
    else:
        print()
    #------------------
    

    #------------------
    urlUserC = f"https://adidas-dev.collibra.com/rest/2.0/users/{userC}"
    responseUserC = requests.get(urlUserC, auth=HTTPBasicAuth(username, password), headers=header)
    dataUserC = responseUserC.json()
    resultsUserC = dataUserC.get("results", [])
    if resultsUserC:
        userInfoC = resultsUserC[0]
        # Process userInfoC if needed
    else:
        print()
    #------------------


    # Call get_first_asset function
    source_asset_Id = first_assetP.get("id", "N/A")
    first_asset = get_first_asset(source_asset_Id)
    
    #aaaa
    if first_asset is not None:
        for asset in first_asset:
            asset_id = asset.get("target", {}).get("id", "N/A")
            isTrue = print_url_response(asset_id)
            if not isTrue:  
                first_asset = get_first_asset(asset_id)
    #------------

 
    if responseProviderInfo.status_code == 200 and responseConsumerInfo.status_code == 200 and responseUserP.status_code == 200 and responseUserC.status_code == 200:
        def print_data_contract_specification():
            print("<strong>Data Contract Specification: 0.0.1</strong>" "<br>")
            print("<strong>INFO" "<br>")
            print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>ID:</strong>", result.get('id'),  "<br>")
            print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Status:</strong>", result.get("status", {}).get("name", "N/A"), "<br>")
            current_datetime = datetime.datetime.now()
            formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M')
            #print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>StartDate:</strong>" , formatted_datetime, "<br>")
            #print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>EndDate:</strong>" "Currently active" "<br>")
            #------------------

            #------------------
            print("<strong><p>&nbsp;</p>PROVIDER<br>")
            print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>DataProduct ID:</strong>", first_assetP.get("id", "N/A"), "<br>")
            print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Creator ID:</strong>", first_assetP.get("createdBy", "N/A"), "<br>")
            creationDate = datetime.datetime.fromtimestamp(first_assetP.get("createdOn") / 1000)
            print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Created on:""</strong>", creationDate, "<br>")
            print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Domain: ID:</strong>", first_assetP.get("domain", {}).get("id", "N/A"), "<br>")
            
            #print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>DataProduct Name:</strong>", first_assetP.get("displayName", "N/A"), "<br>")
            first_name = dataUserP['firstName']
            last_name = dataUserP['lastName']
            #print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Creator Name:</strong>", first_name + ' ' + last_name, "<br>")
            #get("source", {}).get("id", "N/A")
            
            #iteration through get_first_asset and verification if the given ID has a relation of type: if source for
            '''
            source_asset_Id = first_assetP.get("id", "N/A")
            first_asset = get_first_asset(source_asset_Id)#, username, password, header)
            
            isTrue = False
            no_assets_found_message_printed = False
            while not isTrue:
                if first_asset is not None:
                    for asset in first_asset:
                        asset_id = asset.get("target", {}).get("id", "N/A")
                        isTrue = print_url_response(asset_id)#, username, password, header)
                        if  not isTrue:  
                            first_asset = get_first_asset(asset_id)#, username, password, header)
                    no_assets_found_message_printed = False  # Reset the flag since assets are found
                else:
                    if not no_assets_found_message_printed:
                        #print("No assets found in the response.")
                        print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Output Port ID:</strong>" "&nbsp;<p>&nbsp;</p>")
                        print("&nbsp;<p>&nbsp;</p>" "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Output Port Name:</strong>" "&nbsp;<p>&nbsp;</p>")
                        no_assets_found_message_printed = True  # Set the flag to indicate the message was printed
                    break
                '''
            def process_asset(asset_id):
                while asset_id:
                    asset = get_first_asset(asset_id)
                    if asset:
                        for asset_item in asset:
                            target_id = asset_item.get("target", {}).get("id")
                            if target_id and not print_url_response(target_id):
                                asset_id = target_id
                            else:
                                asset_id = None
                    else:
                        if not process_asset.no_assets_found_message_printed:
                            print("<strong>Output Port ID:</strong> N/A")
                            #print("<p><strong>Output Port Name:</strong> N/A</p><br>")
                            process_asset.no_assets_found_message_printed = True
                        break

            process_asset.no_assets_found_message_printed = False
            source_asset_Id = first_assetP.get("id", "N/A")
            process_asset(source_asset_Id)
            #-------------------

            #-------------------
            print("<p>&nbsp;</p>""<strong>CONSUMER</strong>""<br>")
            print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>DataProduct ID:</strong>", first_assetC.get("id", "N/A"), "<br>")
            print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Creator ID:</strong>", first_assetC.get("createdBy", "N/A"), "<br>")
            creationDate = datetime.datetime.fromtimestamp(first_assetC.get("createdOn") / 1000)
            print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Created on:</strong>", creationDate, "<br>")
            print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Domain: ID:</strong>", first_assetC.get("domain", {}).get("id", "N/A"), "<br>")
            
            #print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>DataProduct Name:</strong>", first_assetC.get("displayName", "N/A"), "&nbsp;<p>&nbsp;</p>")
            '''
            first_name = dataUserC['firstName']
            last_name = dataUserC['lastName']
            print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Creator Name:</strong>", first_name + ' ' + last_name, "&nbsp;<p>&nbsp;</p>")
            print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Domain:</strong>", first_assetC.get("domain", "N/A"), "&nbsp;<p>&nbsp;</p>")
            '''
            #---------------------
            
            
            

        # passing the variables to fill in the arguments needed in the function to create the contract asset
        updated_data_contract = {
            "name": f"Contract: {first_assetP.get('name')} -> {first_assetC.get('name')}",
            "displayName": f"Contract:{first_assetP.get('name')}->{first_assetC.get('name')}",
            "domainId": "fcfe595f-a2c4-40f3-977b-4486079e0f60",
            "typeId": "a05583f2-3152-4773-b5ca-62aafed76dcf",
            "statusId": "00000000-0000-0000-0000-000000005008",
            "excludedFromAutoHyperlinking": False
        }

        result = create_contract_asset(username, password, updated_data_contract)

        # variables to fill in the arguments to create the DC to Producer DP relation
        updated_data_P_relation = {
            "sourceId": f"{result.get('id')}", 
            "targetId": f"{first_assetP.get('id')}",
            "typeId": "73d518a0-57b4-46a8-b696-224a2f244320"
        }

        # variables to fill in the arguments to create the DC to Consumer DP relation
        updated_data_C_relation = {
            "sourceId": f"{result.get('id')}",
            "targetId": f"{first_assetC.get('id')}",
            "typeId": "c9a5d38d-7e08-4c13-b817-11f04a3f096c"
        }

        # variables to fill in the arguments to create the DC to output port(s) relation
        info_dcToOutput_relation = {
            "sourceId": f"{result.get('id')}", 
            #"targetId": f"{outputPort.get('id')}",
            #"targetId": "",
            "targetId" : "3f7e22f8-f89e-43c8-8891-69cfb1e50b34", #hard coded, I need to get the output port id
            "typeId": "51c4020d-56ed-4969-a7a5-bad5b0ba89f7"
        }
        
        infoDescription = capture_stdout(print_data_contract_specification)
        

        current_datetime_utc = datetime.datetime.now(pytz.utc)
        midnight_utc = current_datetime_utc.replace(hour=0, minute=0, second=0, microsecond=0)
        timestamp_milliseconds = int(midnight_utc.timestamp()) * 1000
        milliseconds_to_add = 48 * 3600 * 1000


        attributes_to_update = [
            {"typeId": "00000000-0000-0000-0000-000000000207", "value": "Please insert the Contract's Purpose"},
            {"typeId": "00000000-0000-0000-0000-000000000257", "value": f"{timestamp_milliseconds}"},
            {"typeId": "00000000-0000-0000-0000-000000000254", "value": f"{timestamp_milliseconds + milliseconds_to_add}"},
            {"typeId": "00000000-0000-0000-0000-000000000205", "value": "No exceptional conditions for this contract"},

        ]

        updated_responsibilites_P = {
            "roleId": "38bb33bb-cd85-4a3a-bfb7-3afd678957da",
            "ownerId": f"{first_assetP.get('createdBy')}",
            "resourceId": f"{result.get('id')}",
            "resourceType": "Asset"
        }

        updated_responsibilites_C = {
            "roleId": "40146042-0882-4363-a798-c9514ed3cf0a",
            "ownerId": f"{first_assetC.get('createdBy')}",
            "resourceId": f"{result.get('id')}",
            "resourceType": "Asset"
        }

        assetId = result.get('id')
        create_relation(username, password, updated_data_P_relation)
        create_relation(username, password, updated_data_C_relation)
        update_contract_description(username, password, assetId, infoDescription)
        update_attributes(username, password, assetId, attributes_to_update)
        create_relation(username, password, info_dcToOutput_relation)
        create_responsibilities(username, password, updated_responsibilites_P)
        create_responsibilities(username, password, updated_responsibilites_C)
        print("Contract established!")


    else:
    
        print(f"GET Provider Info request failed with status code {responseProviderInfo.status_code}.")
        print(responseProviderInfo.text)
        print(f"GET Consumer Info request failed with status code {responseConsumerInfo.status_code}.")
        print(responseConsumerInfo.text)
        print("ERROR!! Contract NOT established!")

        
    
#remove comments when not using interface.py, for it to work on terminal 
'''
username = config('USERNAME1')
password = config('PASSWORD')
provider = input("Insert the name of the provider Data Product: ")
consumer = input("Insert the name of the consumer Data Product: ")

@contextmanager
def timer():
    start_time = time.time()
    yield
    end_time = time.time()
    print("Execution time:", end_time - start_time, "seconds")

with timer():
    get_data_contract_specification(username, password, provider, consumer)

'''