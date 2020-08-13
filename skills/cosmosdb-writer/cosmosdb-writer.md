# Azure Cognitive Search Python Custom Skill For Cosmos DB Integration (Upsert)

This code is a Python Custom Skill, for Azure Cognitive Search, based on Azure Functions for Python. Using the [Cosmos DB Library](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-cosmosdb-v2?tabs=python), It inserts the input data as elements into a Cosmos DB collection.

## Required steps

1. Follow [this](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python) tutorial.
1. Create one instance of the Content Moderator API in the [Azure Portal](https://ms.portal.azure.com/). You will need to add the access key to the py file of the step below.
1. Use the Python code below as your **__init__.py** file. Customize it with your storage account details, also with your csv file name and target column. As you can see below, my sample csv file target column name is **Term**. That helps the idea that this code will extract pre-defined terms from the documents content.
1. Don't forget to add **azure.functions** to your requirements.txt file.
1. Connect your published custom skill to your Cognitive Search Enrichment Pipeline. Plesae check the section below the code in this file. For more information, click [here](https://docs.microsoft.com/en-us/azure/search/cognitive-search-create-custom-skill-example#connect-to-your-pipeline).

## Python Code

The Python code for this skill is [here](./__init__.py). Please take a minute to read all comments witin the code, where many details and contraints are detailed.

## Add this skill to your Cogntive Search Enrichment Pipeline

Let's assume that organizations were extracted with the Entity Extraction Built-In skill.

```json
 {
            "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
            "name": "cosmosdb-writer",
            "description": "write the data into a Cosmos DB Collection",
            "context": "/document",
            "uri": "your-Pyhton-Azure-Functions-published-URL",
            "httpMethod": "POST",
            "timeout": "PT30S",
            "batchSize": 1,
            "degreeOfParallelism": null,
            "inputs": [
             {
               "name": "text",
               "source": "/document/organizations"
             }
                   ],
        "outputs": [
          {
            "name": "text",
            "targetName": "insertResultStatus"
          }
            ],
            "httpHeaders": {}
           }
```

## Sample Input

Use the JSON input below to test your function. Get familiar with the code behavior in the different situations. 

The test is a tribute to the most popular football club in the world, [Flamengo](https://en.wikipedia.org/wiki/Clube_de_Regatas_do_Flamengo), from Rio de Janeiro. It was founded in 1895 and has over 45 million fans in Brazil alone. The team was [champion](https://www.youtube.com/watch?time_continue=11&v=371FOyquzno) in its two most important matches of 2019, the Brazilian championship and the Copa Libertadores of America.

```json
{
    "values": [
      {
        "recordId": "0",
        "data":
           {
            "text": ["FLAMENGO","VASCO","FLAMENGO","FLUMINENSE","FLAMENGO"]
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
            "text": ["FLAMENGO","Flamengo","flamengo","FLAMENGO"]
           }
      } 
    ]
}
```

## Expected Output

Empty string will be inserted as blank.

```json
{
    "values": [{
        "recordId": "0",
        "data": {
            "text": "OK"
        }
    }, {
        "recordId": "1",
        "data": {
            "text": "OK"
        }
    }, {
        "recordId": "2",
        "data": {
            "text": "OK"
        }
    }]
}
```

