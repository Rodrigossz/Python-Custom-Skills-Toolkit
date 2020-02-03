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
# - The output format is YYYY-MM-DD. Time is removed!!
# - This code uses the datefinder library. Characteristics:
#   1) If the year is detected without month or day, it will be returned with today's month and day.
#   2) If month and date are detected without year, it will return the date with today's year.
#   3) The datafinder library will deal with empty stings and we will handle the outpout format
# - For more details about datefinder: https://datefinder.readthedocs.io/en/latest/

import logging
import azure.functions as func
import re
import datefinder
import json
import datetime

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
        # Getting the dates into an empty Generator
        # Datefinder doesn't handle empty strings
        myString = value['data']['text']
        myString=str(myString)
        if len(myString) == 0:
            myString = ' '
        matches = datefinder.find_dates(myString)

        #First Date only!!!! Change the code if you want all of them.
        for match in matches:
          myDate = match
          # Convert to string
          myDateString = str(myDate)
          break

        # Removing time!!! Change the code if you want it.
        if len(myDateString) > 1:
          myDateString = myDateString[0:10]
        else:
          myDateString = ''

    except:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Could not complete operation for record." }   ]
            })

    return ({
            "recordId": recordId,
            "data": {
                "text": myDateString
                    }
            })


# Testing the function

myInput = {
    "values": [
      {
        "recordId": "0",
        "data":
           {
            "text": ["Flamengo was founded on November 15th 1895"]
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
            "text": ["Flamengo campeão de tudo em 2019!"]
           }
      } 
    ]
}

inputTest = json.dumps(myInput)
compose_response (inputTest)
