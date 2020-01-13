# Azure Cognitive Search Python Custom Skill For Strings Cleaning

This code is a Python Custom Skill, for Azure Cognitive Search, based on Azure Functions for Python. It removes special characters from the input string.

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
# - Letters cases are not changed. But if it is important for you, you can change the code as necessary.

#
# Specific comments
# This code removes special characters like \t and \n from strings
# Accents are not removed. To do it, you need to:
#   import unicode
#   unaccented_string = unidecode.unidecode(accented_string)


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
      # Getting the document text 
      myString = value['data']['text']

      # Replacing special Characters with withe spaces
      myString = re.sub(r'[^\w\s]',' ',myString)
      myString = re.sub(r'\t',' ',myString)
      myString = re.sub(r'\n',' ',myString)
      myString = re.sub(r'  ',' ',myString)


      # Output
      recordId = value['recordId']
      results["values"].append(
            {
            "recordId": recordId,
            "data": {
                "text": myString
                    }
            })
    # We need to make ascii = False to keep accents               
    return json.dumps(results,ensure_ascii=False))
```
## Add this skill to your Cogntive Search Enrichment Pipeline

Your skillset will have this extra section below.

```json
 {
            "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
            "name": "Clean String",
            "description": "Merge Content and File name",
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
            "targetName": "cleanedText"
          }
            ],
            "httpHeaders": {}
           }
```

## Sample Input

One string has special characters, the other one has accents.

```json
{
    "values": [
      {
        "recordId": "0",
        "data":
           {
             "text": "\t\n\tUnited Nations\n\t\n\t"
           }
      },
      {
        "recordId": "1",
        "data":
           {
             "text": "Nação Rubro Negra"
           }
      },      
      
    ]
}
```

## Sample Output

In the first string, special characters are removed. Nothing happens with the second string.

```json
{
    "values": [
        {
            "recordId": "0",
            "data": {
                "text": "United Nations"
            }
        },
        {
            "recordId": "1",
            "data": {
                "text": "Nação Rubro Negra"
            }
        }
    ]
}
```

