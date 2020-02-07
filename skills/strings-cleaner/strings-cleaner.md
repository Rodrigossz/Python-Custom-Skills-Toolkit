# Azure Cognitive Search Python Custom Skill For Strings Cleaning

This code is a Python Custom Skill, for Azure Cognitive Search, based on Azure Functions for Python. It removes special characters from the input string.

## Required steps

1. Follow [this](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python) tutorial.
1. Use the Python code below as your **__init__.py** file. Customize it with your storage account details, also with your csv file name and target column. As you can see below, my sample csv file target column name is **Term**. That helps the idea that this code will extract pre-defined terms from the documents content.
1. Don't forget to add **azure.functions** to your requirements.txt file.
1. Connect your published custom skill to your Cognitive Search Enrichment Pipeline. Plesae check the section below the code in this file. For more information, click [here](https://docs.microsoft.com/en-us/azure/search/cognitive-search-create-custom-skill-example#connect-to-your-pipeline).

## Python Code

The Python code for this skill is [here](./__init__.py). 

## Add this skill to your Azure Cogntive Search Enrichment Pipeline

Your skillset will have this extra section below.

```json
 {
            "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
            "name": "Strings Cleaner",
            "description": "Cleans special characters",
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

Use the JSON input below to test your function. Get familiar with the code behavior in the different situations. 

This test text is a tribute to the most popular football club in the world, [Flamengo](https://en.wikipedia.org/wiki/Clube_de_Regatas_do_Flamengo), from Rio de Janeiro. It was founded in 1895 and has over 45 million fans in Brazil alone. The team was [champion](https://www.youtube.com/watch?time_continue=11&v=371FOyquzno) in its two most important matches of 2019, the Brazilian championship and the Copa Libertadores of America.

```json
{
    "values": [
      {
        "recordId": "0",
        "data":
           {
            "text": ["Flamengo Campeão!!!!###"]
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
            "text": ["Nação Rubro Negra"]
           }
      } 
    ]
}
```

## Expected Output

```json
{
    "values": [{
        "recordId": "0",
        "data": {
            "text": "Flamengo Campeão"
        }
    }, {
        "recordId": "1",
        "data": {
            "text": ""
        }
    }, {
        "recordId": "2",
        "data": {
            "text": "Nação Rubro Negra"
        }
    }]
}
```

