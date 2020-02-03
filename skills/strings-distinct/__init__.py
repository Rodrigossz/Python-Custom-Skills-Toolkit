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
# - This code removes duplicates from a list.
# - This code is case sensitive: "Flamengo" is different from  "FLAMENGO" and both will be returned.

import logging
import azure.functions as func
import json

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


        # Cleaning the list
        myStringList = list(dict.fromkeys(myStringList))

    except:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Could not complete operation for record." }   ]
            })

    return ({
            "recordId": recordId,
            "data": {
                "text": myStringList
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
