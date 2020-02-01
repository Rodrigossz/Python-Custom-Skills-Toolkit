# Azure Cognitive Search Python Custom Skill For CSV Lookups

This code is a Python Custom Skill, for Azure Cognitive Search, based on Azure Functions for Python. It extracts all terms of a csv file that exists in the input string. There must be one term per line in the csv file. And the csv file must have only one column.

## Required steps

1. Follow [this](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python) tutorial.
1. Use the Python code below as your **__init__.py** file. Customize it with your storage account details, also with your csv file name and target column. As you can see below, my sample csv file target column name is **Term**. That helps the idea that this code will extract pre-defined terms from the documents content.
1. Don't forget to add **azure.functions** to your requirements.txt file.
1. Connect your published custom skill to your Cognitive Search Enrichment Pipeline. Plesae check the section below the code in this file. For more information, click [here](https://docs.microsoft.com/en-us/azure/search/cognitive-search-create-custom-skill-example#connect-to-your-pipeline).

## Python Code

The Python code for this skill is [here](./__init__.py). 

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

