# Azure Cognitive Search Python Custom Skill Duplicates removal - Distinct

This code is a Python Custom Skill, for Azure Cognitive Search, based on Azure Functions for Python. It removes duplicated terms from the input text. 

It is specially useful when you are processing per page and the same entities or key phrases are extracted in all pages, creating duplicated values within your enrichment pipeline. You can use this skill to clean it before the data push into the Azure Cognitive Search Index. Details:

+ The Expected input is something like "text": "[BRAZIL],[BRAZIL],[ARGENTINA],[BRAZIL]"
+ The output will be "text": "[BRAZIL],[ARGENTINA]"
+ This code is case sensitive. Change it if you need.

## Required steps

1. Follow [this](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python) tutorial.
1. Use the Python code below as your **__init__.py** file. Customize it with your storage account details, also with your csv file name and target column. As you can see below, my sample csv file target column name is **Term**. That helps the idea that this code will extract pre-defined terms from the documents content.
1. Don't forget to add **azure.functions** to your requirements.txt file.
1. Connect your published custom skill to your Cognitive Search Enrichment Pipeline. Plesae check the section below the code in this file. For more information, click [here](https://docs.microsoft.com/en-us/azure/search/cognitive-search-create-custom-skill-example#connect-to-your-pipeline).
1. If you need errors and warnings management, use [this](https://docs.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-interface#web-api-custom-skill-interface) link as a reference and change the code to add it.

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
# Expected input is something like "text": "[BRAZIL],[BRAZIL],[ARGENTINA],[BRAZIL]"
# Output will be "text": "[BRAZIL],[ARGENTINA]"
# This code is case sentive!! Change it if you need.

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
    
    # Prepare the Output before the loop
    results = {}
    results["values"] = []

    for value in values:
        # Getting the items from the values/data/text
        myStringList = []
        myStringList = value['data']['text']


        # Expected input is something like "text": "[BRAZIL],[BRAZIL],[ARGENTINA],[BRAZIL]"
        # Output will be "text": "[BRAZIL],[ARGENTINA]"
        myStringList = list(dict.fromkeys(myStringList))

        
        # Output
        recordId = value['recordId']
        results["values"].append(
            {
            "recordId": recordId,
            "data": {
                "text": myStringList
                    }
            })
                    
    return json.dumps(results,ensure_ascii=False)
```

## Add this skill to your Cogntive Search Enrichment Pipeline

Let's say that we are extracting locations per page. IF the same location is present in each page, it will be duplicated within your enrichment pipeline.

```json
 {
            "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
            "name": "strings-distinc",
            "description": "REMOVE duplicates elements from the input array",
            "context": "/document",
            "uri": "your-Pyhton-Azure-Functions-published-URL",
            "httpMethod": "POST",
            "timeout": "PT30S",
            "batchSize": 1,
            "degreeOfParallelism": null,
            "inputs": [
             {
               "name": "text",
               "source": "/document/locations/*"
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
}
```

## Sample Input

The input has multiple repetitions.

```json
{
    "values": [
      {
        "recordId": "0",
        "data":
           {
            "text": ["BRAZIL","BRAZIL","ARGENTINA","BRAZIL","Brazil"]
           }
      }     
      
    ]
}
```

## Sample Output

Duplicates are removed. This code is case sensitive.

```json
{
    "values": [
        {
            "recordId": "0",
            "data": {
            "text": ["BRAZIL","ARGENTINA","Brazil"]
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