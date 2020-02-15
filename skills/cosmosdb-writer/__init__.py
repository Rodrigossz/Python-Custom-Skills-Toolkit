# Standard for all skills:
# - Author: Rodrigo Souza - https://www.linkedin.com/in/rodrigossz/
# - This code is an Azure Cognitive Search Python Custom Skill.
# - The output is the "text" element within the "data" section of the json file.
# - For production environments add all best practices, logging, and error management that you need.
# - Letters cases are not changed.
# - All JSON files are returned with the original accents. For that, we use ensure_ascii=False.
# - You can find other Python Custom Skills here: https://github.com/Rodrigossz/Python-Custom-Skills-Toolkit
#
# Specific comments
# - This code removes duplicates from a list. It is case sensitive: "Flamengo" is different from  "FLAMENGO" and both will be inserted.
# - This custom skill gets the input, maybe a list from keyPhrases or entities extraction, and loads EACH ELEMENT as a document in a CosmosDb Collection
# - Change the code as you want: You can group the elements and insert one document per Cognitive Search document. That's a very good idea, BTW. 
# - This code works great with CosmosDb Emulator! Check it out! https://docs.microsoft.com/en-us/azure/cosmos-db/local-emulator#installation

import logging
import azure.functions as func
import json
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import uuid


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        body = json.dumps(req.get_json())
    except ValueError:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )
    
    if body:
        result = compose_response(body)
        return func.HttpResponse(result, mimetype="application/json")
    else:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )


def compose_response(json_data):
    values = json.loads(json_data)['values']
    
    # Prepare the Output before the loop
    results = {}
    results["values"] = []
    
    for value in values:
        outputRecord = transform_value(value)
        if outputRecord != None:
            results["values"].append(outputRecord)
    # Keeping the original accentuation with ensure_ascii=False
    return json.dumps(results, ensure_ascii=False)

## Perform an operation on a record
def transform_value(value):
    try:
        recordId = value['recordId']
    except AssertionError  as error:
        return None

    # Validate the inputs
    try:         
        assert ('data' in value), "'data' field is required."
        data = value['data']        
        assert ('text' in data), "'text' field is required in 'data' object."
    except AssertionError  as error:
        return (
            {
            "recordId": recordId,
            "data":{},
            "errors": [ { "message": "Error:" + error.args[0] }   ]
            })

    try:                
        # Getting the items from the values/data/text
        myStringList = []
        myStringList = value['data']['text']

        # Cleaning the list, removing duplicates
        myStringList = list(dict.fromkeys(myStringList))

        # Now let's insert one document for each organization in the list.
        # Change as you need!!

        # Initialize the Cosmos client
        # Add your own data or use a better method to get this information
        endpoint = "your-CosmosDb-URI"
        key = 'your-CosmosDb-key'

        # <create_cosmos_client>
        client = CosmosClient(endpoint, key)
        # </create_cosmos_client>

        # Create a database
        # Use the name that you want.
        # <create_database_if_not_exists>
        database_name = 'MyCustomSkillData'
        database = client.create_database_if_not_exists(id=database_name)
        # </create_database_if_not_exists>

        # Create a container
        # Customize as you want: person names, key phrases, etc.
        # Or you can insert the list under a document, keeping parity between CosmosDb and Azure Cognitive Search
        # Using a good partition key improves the performance of database operations.
        # Also, change the partition key as you want/need.
        # <create_container_if_not_exists>
        container_name = 'Organizations'
        container = database.create_container_if_not_exists(
            id=container_name, 
            partition_key=PartitionKey(path="/name"),
            offer_throughput=400
        )
        # </create_container_if_not_exists>

         # <create_item>
        for item in myStringList:
            newDoc = {
                'id': str(uuid.uuid4()),
                'name': item
            }
            container.create_item(body=newDoc)
        # </create_item>

    except:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Could not complete operation for record." }   ]
            })

    return ({
            "recordId": recordId,
            "data": {
                "text": "OK"
                    }
            })


# Testing the function

myInput = {
    "values": [
      {
        "recordId": "0",
        "data":
           {
            "text": ["FLAMENGO","VASCO","FLAMENGO","FLUMINENSE","FLAMENGO"]
           }
      } ,
        {
        "recordId": "1",
        "data":
           {
            "text": [""]
           }
      } ,    
      {
        "recordId": "2",
        "data":
           {
            "text": ["FLAMENGO","Flamengo","flamengo","FLAMENGO"]
           }
      } 
    ]
}

inputTest = json.dumps(myInput)
compose_response (inputTest)
