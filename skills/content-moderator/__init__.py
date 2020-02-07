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
# - This detects PII from the input strings.
# - Content Moderator API input limit is 1024 characters, that's why we have substring.
# - Characters after 1024 positions will be ignored. Change the code and add a loop if you need to process the all string.  
# - This skill returns True or False. Change the code if you need anything different.
# - This code is Python 3.x only!!!!!

import logging
import azure.functions as func
import json
import re
import http.client, urllib.request, urllib.parse, urllib.error, base64


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
        # Getting the document text 
        # Only the 1024 first characters!!!!!!
        # To process the all string, change the code as you need.
        myString = value['data']['text']
        myString = str(myString)[:1023]

        # Replacing special Characters with withe spaces
        # The order matters!! Be careful!!
        myString = re.sub(r'\r\n',' ',myString)
        myString = re.sub(r'\t',' ',myString)
        myString = re.sub(r'\n',' ',myString)
 
        #To avoid the API to process no data. 
        if (myString != '') and (myString != ' '):

            # Using the Content Moderator API
            ########### Python 3.x #############
            headers = {
            # Request headers
            # ACTION REQUIRED!!!
            # REPLACE THE STRING BELOW WITH YOUR KEY!!
            'Content-Type': 'text/plain',
            'Ocp-Apim-Subscription-Key': 'your-content-moderator-api-key',
            }

            params = urllib.parse.urlencode({
            # Request parameters
            # Unfortunately, the Content Moderator uses 3 letters for language code
                #'autocorrect': 'False',
                'PII': 'True',
                #'listId': 'False',
                #'classify': 'False',
                'language': 'eng'
            })

            # ACTION REQUIRED!!!
            # Replace the string your-content-moderator-azure-region with the region code that you used to create the API
            conn = http.client.HTTPSConnection('your-content-moderator-azure-region.api.cognitive.microsoft.com')
            conn.request("POST", "/contentmoderator/moderate/v1.0/ProcessText/Screen?%s" % params, myString, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()

            # returing the data 
            myString = str(data)

        # We are just detecting if there is PII, returning True or False.
        # Change the code as you need

        if myString.find('PII') > 0:
            myString = 'True'
        else:
            myString = 'False'

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
            "text": ["Flamengo phone numer is 206-999-1981. The email address is contato@flamengo.com ."]
           }
      } ,
        {
        "recordId": "1",
        "data":
           {
            "text": ["Flamengo is the new champion!!"]
           }
      } ,
    {
        "recordId": "2",
        "data":
           {
            "text": []
           }
      } 
    ]
}

inputTest = json.dumps(myInput)
compose_response (inputTest)
