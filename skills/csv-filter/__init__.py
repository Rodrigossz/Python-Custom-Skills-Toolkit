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
# - This skill filters (removes) the terms in the csv file from the string.
# - There must be one term per line in the csv file. 
# - And the csv file must have only one column.
# - In other words, it is a csv file without any column in it. Any column will be considerated part of the ter.
# - This code opens the terms.csv file in the same folder of the __init__.py file.
# - File name is always terms.csv . If you want another name, chage it below.
# - All data from both sources, input and csv, are converted to lower case for the strings comparison. Orinal case is returned.
# - Only the matches are returned.

import logging
import azure.functions as func
import csv
import json
import re
import os

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

    # Get reference data - csv file. Any plafform, any OS. 
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    myFile=os.path.join(__location__, 'terms.csv')
    myFile=os.path.normpath(myFile)
    with open (myFile,'r', encoding='latin-1') as csvList:
        myList = list(csv.reader(csvList))
    
    for value in values:
        outputRecord = transform_value(value,myList)
        if outputRecord != None:
            results["values"].append(outputRecord)
    # Keeping the original accentuation with ensure_ascii=False
    return json.dumps(results, ensure_ascii=False)

## Perform an operation on a record
def transform_value(value,myList):
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
        # Preparing the data output, reading the data
        recordId = value['recordId']
        text = value['data']['text']

        # Adding and extra white spaces because I also add one for the terms
        text=' '+text+' '

        # Removing pontuaction, also because on the white spaces. 
        # A term followed by comma or other pontuaction would not be extracted because on the white spaces
        text = re.sub(r'[^\w\s]','',text)

        #Now let's process for each term in the CSV
        for term in myList:

        #Convert to string and add spaces to avoid things like 'Africa' been removed from 'African'
          myStr=' '+str(term[0])+' '
          if text.lower().find(myStr.lower()) >= 0:
            #remove the terms and white spaces that may have been left behind
            text= re.sub(myStr, '', text)
            text=text.strip()


    except:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Could not complete operation for record." }   ]
            })

    return ({
            "recordId": recordId,
            "data": {
                "text": text
                    }
            })


# Testing the function, forcing one error for the second record. 
# Third record is an empty string. It will work.
# The sample csv content is:
# FLAMENGO
# BARCELONA
# REAL MADRID
# MANCHESTER UNITED
# LIVERPOOL
# MILAN
# JUVENTUS


myInput = {
    "values": [
      {
        "recordId": "0",
        "data":
           {
             "text": "FLAMENGO is the new champion"
           }
      },
        
      {
        "recordId": "1",
        "data":
           {
            "text": "FLAMENGO beat LIVERPOOL in the 1981 World Cup final."
            }
      },
        {
        "recordId": "2",
        "data":
           {
            "text": ""

            }
        },


    ]
}

inputTest = json.dumps(myInput)
compose_response (inputTest)
