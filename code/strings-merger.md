# Azure Cognitive Search Python Custom Skill For Strings Concatenation

This code is a Python Custom Skill, for Azure Cognitive Search, based on Azure Functions for Python. It merges 2 strings in a third one, useful when you want to concatenate, within an Enrichment Pipeline, the file name or path with the content. This skill is indicated for scenarios when the file name or path have dates, organizations, names, or key phrases. 

Until January 2020, you can't do this merge usint the Built In Merge Skill since you won't have the required offistes. I just suggested this feature as a built in capability. For now, this code is the alternative.

## Required steps

1. Follow [this](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python) tutorial.
1. Use the Python code below as your **__init__.py** file. Customize it with your storage account details, also with your csv file name and target column. As you can see below, my sample csv file target column name is **Term**. That helps the idea that this code will extract pre-defined terms from the documents content.
1. Don't forget to add **azure.functions** to your requirements.txt file.
1. Connect your published custom skill to your Cognitive Search Enrichment Pipeline. Plesae check the section below the code in this file. For more information, click [here](https://docs.microsoft.com/en-us/azure/search/cognitive-search-create-custom-skill-example#connect-to-your-pipeline).

## Python Code

```python
# Header - Standard for all skills:
# - Author: Rodrigo Souza - https://www.linkedin.com/in/rodrigossz/
# - This code is an Azure Cognitive Search Python Custom Skill.
# - The output is the "text" element within the "data" section of the json file.
# - For production environments add all best practices, logging, and error management that you need.
# - Letters cases are not changed.
# - All JSON files are returned with the original accents. For that, we use ensure_ascii=False.
#
# Specific comments
# This code concatenates 2 strings. 
# I Use white spaces to don't concatenatr words without a separation.

import logging
import azure.functions as func
import re
import json

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
    
    values = json.loads(json_data)['values']
    results = {}
    results["values"] = []

    for value in values:
        
        # Testing for empty strings - Customize as you want. Returning white spaces
        if (not string1):
            string1 = ' '

        if (not string2):
            string2 = ' '
       
        # merging, with white spaces addiction
        mergedStrings = " "+ string1 + " "+ string2 + " "
        recordId = value['recordId']
        results["values"].append(
                {
                "recordId": recordId,
                "data": {
                    "text": mergedStrings
                        }
                })
                    
    return json.dumps(results,ensure_ascii=False))
```

## Add this skill to your Cogntive Search Enrichment Pipeline

Your skillset will have this extra section below.

```json
 {
            "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
            "name": "Concatenate Strings",
            "description": "Merge Content and File name",
            "context": "/document",
            "uri": "your-Pyhton-Azure-Functions-published-URL",
            "httpMethod": "POST",
            "timeout": "PT30S",
            "batchSize": 1,
            "degreeOfParallelism": null,
            "inputs": [
             {
               "name": "string1",
               "source": "/document/metadata_storage_name"
             },
             {
               "name": "string2",
               "source": "/document/content"
             }
                   ],
        "outputs": [
          {
            "name": "text",
            "targetName": "concatenatedText"
          }
            ],
            "httpHeaders": {}
           }
```

## Sample Input

```json
{
    "values": [
      {
        "recordId": "0",
        "data":
           {
             "string1": "Flamengo is",
             "string2": "the new champion"
           }
      },
        
      {
        "recordId": "1",
        "data":
           {
            "string1": "Flamengo_Libertadores_2019.jpg",
            "string2": "Champion"
            }
      }
    ]
}
```

## Sample Output

```json
{
    "values": [
        {
            "recordId": "0",
            "data": {
                "terms": " Flamengo is the new champion "
            }
        },
        {
            "recordId": "1",
            "data": {
                "terms": " Flamengo Libertadores 2019 jpg Champion "
            }
        }
    ]
}
```

