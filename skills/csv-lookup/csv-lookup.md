# Azure Cognitive Search Python Custom Skill For CSV Lookups

This code is a Python Custom Skill, for Azure Cognitive Search, based on Azure Functions for Python. It extracts all terms of a csv file that exists in the input string. There must be one term per line in the csv file. And the csv file must have only one column.

## Required steps

1. Follow [this](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python) tutorial.
1. Use the Python code below as your **__init__.py** file. Customize it with your storage account details, also with your csv file name and target column. As you can see below, my sample csv file target column name is **Term**. That helps the idea that this code will extract pre-defined terms from the documents content.
1. Don't forget to add **azure.functions** to your requirements.txt file.
1. Connect your published custom skill to your Cognitive Search Enrichment Pipeline. Plesae check the section below the code in this file. For more information, click [here](https://docs.microsoft.com/en-us/azure/search/cognitive-search-create-custom-skill-example#connect-to-your-pipeline).

## Python Code

The Python code for this skill is [here](./__init__.py). 

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
# Only the matches are returned.


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
      outputList=[]
      recordId = value['recordId']
      text = value['data']['text']

      # Adding and extra white spaces because I also add one for the terms
      text=' '+text+' '

      # Removing pontuaction, also because on the white spaces. 
      # A term followed by comma or other pontuaction would not be extracted because on the white spaces
      text = re.sub(r'[^\w\s]','',text)

      for term in myList:
          #Convert to string and add spaces to avoid things like 'Africa' been extracted from 'African'
          myStr=' '+str(term[0])+' '
          if text.lower().find(myStr.lower()) >= 0:
            #remove the white spaces
            myStr=myStr.strip()
            outputList.append(myStr)
      results["values"].append(
              {
              "recordId": recordId,
              "data": {
                  "text": outputList
                      }
              })
                    
    return json.dumps(results,ensure_ascii=False)
```

## Add this skill to your Cogntive Search Enrichment Pipeline

```json
 {
            "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
            "name": "csv-lookup",
            "description": "Find the clubs I care about",
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
            "targetName": "clubs"
          }
            ],
            "httpHeaders": {}
           }
```

## Sample Input

Use the JSON input below to test your function. Get familiar with the code behavior in the different situations. 

The test is a tribute to the most popular football club in the world, [Flamengo](https://en.wikipedia.org/wiki/Clube_de_Regatas_do_Flamengo), from Rio de Janeiro. It was founded in 1895 and has over 45 million fans in Brazil alone. The team was [champion](https://www.youtube.com/watch?time_continue=11&v=371FOyquzno) in its two most important matches of 2019, the Brazilian championship and the Copa Libertadores of America.

The sample csv has a small list of the biggest football clubs in the world:

```csv
FLAMENGO
BARCELONA
REAL MADRID
MANCHESTER UNITED
LIVERPOOL
MILAN
JUVENTUS
```

```json
{
    "values": [
      {
        "recordId": "0",
        "data":
           {
             "text": "Flamengo is the new champion"
           }
      },
        
      {
        "recordId": "1",
        "data":
           {
            "text": "Flamengo beat Liverpool in the 1981 World Cup final."
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
```

## Expected Output

```json
{
    "values": [{
        "recordId": "0",
        "data": {
            "text": ["FLAMENGO"]
        }
    }, {
        "recordId": "1",
        "data": {
            "text": ["FLAMENGO", "LIVERPOOL"]
        }
    }, {
        "recordId": "2",
        "data": {
            "text": []
        }
    }]
}
```

