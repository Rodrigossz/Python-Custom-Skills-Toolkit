# Azure Cognitive Search Python Custom Skill For CSV Filtering

This code is a Python Custom Skill, for Azure Cognitive Search, based on Azure Functions for Python. It removes all terms of a csv file that exists in the input string. The input string is returned without the terms to be filtered. There must be one term per line in the csv file. And the csv file must have only one column.

## Required steps

1. Follow [this](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python) tutorial.
1. Use the Python code below as your **__init__.py** file. Customize it with your storage account details, also with your csv file name and target column. As you can see below, my sample csv file target column name is **Term**. That helps the idea that this code will extract pre-defined terms from the documents content.
1. Don't forget to add **azure.functions** to your requirements.txt file.
1. Connect your published custom skill to your Cognitive Search Enrichment Pipeline. Plesae check the section below the code in this file. For more information, click [here](https://docs.microsoft.com/en-us/azure/search/cognitive-search-create-custom-skill-example#connect-to-your-pipeline).

## Errors and Warnings

If you need errors and warnings management, use [this](https://docs.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-python) link as a reference and change the code to add it.

## Python Code

```python
# Header - Standard for all skills:
# - Author: Rodrigo Souza - https://www.linkedin.com/in/rodrigossz/
# - This code is an Azure Cognitive Search Python Custom Skill.
# - The output is the "text" element within the "data" section of the json file.
# - For production environments add all best practices, logging, and error management that you need.
# - Letters cases are not changed. But if it is important for you, you can change the code as necessary.
# - All JSON files are returned with the original accents. For that, we use ensure_ascii=False.
# - Errors and warnings are not returned to the enrichment pipeline. Chage the code as you need to add this feature.
#
# Specific comments
# There must be one term per line in the csv file. 
# And the csv file must have only one column.
# In other words, it is a csv file without any column in it. Any column will be considerated part of the ter.
# This code opens the orgs.csv file in the same folder of the __init__.py file.
# File name is always terms.csv . If you want another name, chage it below.
# All data from both sources, input and csv, are converted to lower case for the strings comparison. Orinal case is returned.
# The input string is returned, without the the filtered terms.

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
        pass

    if body:
        return func.HttpResponse(run(body), mimetype="application/json")
    else:
        return func.HttpResponse(
             "Invalid Body.",
             status_code=555
        )


def run(json_data):

  # Get reference data - csv file 
  # Any plafform, any OS
  __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
  myFile=os.path.join(__location__, 'terms.csv')
  myFile=os.path.normpath(myFile)

  with open (myFile,'r', encoding='latin-1') as csvList:
    myList = list(csv.reader(csvList))

    # Get the input data
    values = json.loads(json_data)['values']

    # Preparing output
    results = {}
    results["values"] = []
            
    # Process row by row
  
    for value in values:
      recordId = value['recordId']
      text = value['data']['text']

      for term in myList:
          #Convert to string 
          myStr=str(term[0])
          if text.lower().find(myStr.lower()) >= 0:
            #remove the terms
            text= re.sub(myStr, '', text)
      results["values"].append(
              {
              "recordId": recordId,
              "data": {
                  "text": outputStr
                      }
              })
                    
    return json.dumps(results,ensure_ascii=False)
```

## Add this skill to your Cogntive Search Enrichment Pipeline

Let's say that your terms are some countrires of the word. You CSV will have the structure below:

Brazil
Argentina
Canadá
United States

One country and one column per line, no commas. You skillset will have something like:

```json
 {
            "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
            "name": "csv-filter",
            "description": "REMOVE the Countries I Don't care about",
            "context": "/document",
            "uri": "your-Pyhton-Azure-Functions-published-URL",
            "httpMethod": "POST",
            "timeout": "PT30S",
            "batchSize": 1,
            "degreeOfParallelism": null,
            "inputs": [
             {
               "name": "text",
               "source": "/document/content"
             }
                   ],
        "outputs": [
          {
            "name": "text",
            "targetName": "filteredText"
          }
            ],
            "httpHeaders": {}
           }
```

## Sample Input

One string has 2 dates, the second one has only the year.

```json
{
    "values": [
      {
        "recordId": "0",
        "data":
           {
             "text": "Brazil is bigger than the US if you don't count on Alaska. Argentina is not that big."
           }
      },
      {
        "recordId": "1",
        "data":
           {
             "text": "I live in the United States of America"
           }
      }
    ]
}
```

## Sample Output

From the first string, two countries are returned. US is not one of the lines of the file. Only exact matches are returned. 

```json
{
    "values": [
        {
            "recordId": "0",
            "data": {
                "text": "is bigger than the US if you don't count on Alaska. is not that big."
            }
        },
        {
            "recordId": "1",
            "data": {
                "text": "I live in the of America"
            }
        }
    ]
}
```

