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
# - Using  mkt = 'en-US', US EN Wikipedia. Change as you want.
# - You can use the language code of the enrichment pipeline as a parameter
# - This skill returns the description of the input. You can change for URL or many other options returned by the API
# - This code is Python 3.x only!!!!!
# - For more information, go to https://docs.microsoft.com/en-us/azure/cognitive-services/bing-entities-search/quickstarts/python

import logging
import azure.functions as func
import json
import http.client, urllib.parse


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
        # Getting the Search Entity
        myString = str(value['data']['text'])
        
        # Search Parameters
        subscriptionKey = '3d5f223640594a23a30ec3c99a195862'
        host = 'mybingentitysearch.cognitiveservices.azure.com'
        path = '/bing/v7.0/entities'
        mkt = 'en-US' # Change as you want  
        query = myString
        params = '?mkt=' + mkt + '&q=' + urllib.parse.quote (query)

        # Function to call the API
        def get_suggestions ():
            headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
            conn = http.client.HTTPSConnection (host)
            conn.request ("GET", path + params, None, headers)
            response = conn.getresponse ()
            return response.read()

        result = get_suggestions ()
        # You can get many other things back, as the url. We are getting the description
        # Example: myString = json.dumps(json.loads(result)['entities']['value'][0]['url'])
        myString = json.dumps(json.loads(result)['entities']['value'][0]['description'])

    except:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Could not complete operation for record." }   ]
            })

    return ({
            "recordId": recordId,
            "data": {
                "text": myString
                    }
            })
    


# Testing the function


myInput = {
    "values": [
      {
        "recordId": "0",
        "data":
           {
            "text": "Flamengo"
           }
      }
     
    ]
}

inputTest = json.dumps(myInput)
compose_response (inputTest)