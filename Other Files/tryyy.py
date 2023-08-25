import requests
from requests.auth import HTTPBasicAuth
from decouple import config


username = config('USERNAME1')
password = config('PASSWORD')
header = {
    "Content-Type" : "application/json"
}

urlDP_Represents_Schema = "https://adidas-dev.collibra.com/rest/2.0/relations?offset=0&limit=0&countLimit=-1&relationTypeId=00000000-0000-0000-0000-000000007038&sourceTargetLogicalOperator=AND"
urlSchema_Contains_Table = "https://adidas-dev.collibra.com/rest/2.0/relations?offset=0&limit=0&countLimit=-1&relationTypeId=00000000-0000-0000-0000-000000007043&sourceTargetLogicalOperator=AND"
urlTable_IsSourceFor_Table = "https://adidas-dev.collibra.com/rest/2.0/relations?offset=0&limit=0&countLimit=-1&relationTypeId=362efbbd-f0f1-4d65-8bd6-00fc19f87d32&sourceTargetLogicalOperator=AND"


responseDP_Represents_Schema = requests.get(urlDP_Represents_Schema, auth=HTTPBasicAuth(username, password), headers=header)
dp_represents_schema_dict = {}

responseSchema_Contains_Table = requests.get(urlSchema_Contains_Table, auth=HTTPBasicAuth(username, password), headers=header)
schema_contains_table_dict = {}

responseTable_IsSourceFor_Table = requests.get(urlTable_IsSourceFor_Table, auth=HTTPBasicAuth(username, password), headers=header)
table_IsSourceFor_table_dict = {}

#--

#--
if responseSchema_Contains_Table.status_code == 200 and responseDP_Represents_Schema.status_code == 200 and responseTable_IsSourceFor_Table.status_code == 200:
    
    dp_represents_schema = responseDP_Represents_Schema.json()
    dataDP_represents_schema = dp_represents_schema.get("results", [])

    schema_contains_table = responseSchema_Contains_Table.json()
    dataSchema_Contains_Table = schema_contains_table.get("results", [])

    table_IsSourceFor_table = responseTable_IsSourceFor_Table.json()
    dataTable_IsSourceFor_table = table_IsSourceFor_table.get("results", [])

    #--------------
    if dataDP_represents_schema:
        for result in dataDP_represents_schema:
            target_schema_id = result.get("target", {}).get("id", "N/A")
            target_schema_name = result.get("target", {}).get("name", "N/A")

            source_DP_id = result.get("source", {}).get("id", "N/A")
            source_DP_name = result.get("source", {}).get("name", "N/A")

            dp_represents_schema_dict[target_schema_id] = (source_DP_id, source_DP_name, target_schema_name)
            
    else:
        print("No assets found in the response.")
    
    #print(dp_represents_schema_dict)
    #---------------

    #---------------
    if dataSchema_Contains_Table:
        for result in dataSchema_Contains_Table:
            target_table_id = result.get("target", {}).get("id", "N/A")
            target_table_name = result.get("target", {}).get("name", "N/A")

            source_schema_id = result.get("source", {}).get("id", "N/A")
            source_schema_name = result.get("source", {}).get("name", "N/A")

            schema_contains_table_dict[target_table_id] = (source_schema_id, source_schema_name, target_table_name)
            
    else:
        print("No assets found in the response.")
    
    #print(schema_contains_table_dict)
    #--------------
    
    #--------------
    if dataTable_IsSourceFor_table:
            for result in dataTable_IsSourceFor_table:
                target_output_table_id = result.get("target", {}).get("id", "N/A")
                target_output_table_name = result.get("target", {}).get("name", "N/A")

                source_table_id = result.get("source", {}).get("id", "N/A")
                source_table_name = result.get("source", {}).get("name", "N/A")

                table_IsSourceFor_table_dict[target_output_table_id] = (source_table_id, source_table_name, target_output_table_name)
    else:
        print("No assets found in the response.")
    
    #print(table_IsSourceFor_table_dict)
    #--------------

    def find_tableID_by_schemaID(dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key
        return None

    '''
    dpHasSchema = []
    for target_schema_id in dp_represents_schema_dict.keys():
        #print(target_schema_id)
        source_schema_id = dp_represents_schema_dict[target_schema_id][0]
        #print(source_schema_id)
        #if source_schema_id == target_schema_id:
            #dpHasSchema.append((target_schema_id, source_schema_id.key))
        matching_key = None
        for key, value in schema_contains_table_dict.items():
            if value == source_schema_id:
                matching_key = key
                break
        # Check if a matching key was found
        if matching_key is not None:
            # Append the matching (target_schema_id, source_schema_id) tuple with the corresponding key to the list
            dpHasSchema.append((target_schema_id, matching_key))
        elif source_schema_id == target_schema_id:
            # Append the (target_schema_id, source_schema_id) tuple with source_schema_id as the key
            dpHasSchema.append((target_schema_id, source_schema_id))
    print(dpHasSchema)
    '''
    '''
    matching_source_DP_ids = set()
    # Loop through dataDP_represents_schema (dict1)
    if dataDP_represents_schema:
        for result in dataDP_represents_schema:
            # Extract target_schema_id and source_DP_id
            target_schema_id = result.get("target", {}).get("id", "N/A")
            source_DP_id = result.get("source", {}).get("id", "N/A")

            # Check if the source_DP_id is present in dataSchema_Contains_Table (dict2)
            for schema_contains_result in dataSchema_Contains_Table:
                if schema_contains_result.get("source", {}).get("id", "N/A") == target_schema_id:
                    target_table_id = schema_contains_result.get("target", {}).get("id", "N/A")

                    # Check if the target_table_id is present in dataTable_IsSourceFor_table (dict3)
                    for table_source_result in dataTable_IsSourceFor_table:
                        if table_source_result.get("source", {}).get("id", "N/A") == source_table_id:
                            target_output_table_id = table_source_result.get("target", {}).get("id", "N/A")

                            # Append the matching source_DP_id to the list
                        #matching_source_DP_ids.add(source_DP_id, target_schema_id, source_schema_id, target_table_id, source_table_id, target_output_table_id)
                        matching_source_DP_ids.add((source_DP_id, target_schema_id, source_DP_id, target_table_id, source_table_id, target_output_table_id))

    # Now matching_source_DP_ids set contains the tuples with matching IDs
    print(matching_source_DP_ids)

    """
    matching_source_DP_ids_list = list(matching_source_DP_ids)
    print(matching_source_DP_ids_list)
    """
    '''
    #print(table_IsSourceFor_table_dict)
else:
    print("Failed to retrieve data from the API.")