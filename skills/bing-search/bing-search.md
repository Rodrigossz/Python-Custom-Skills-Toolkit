# Azure Cognitive Search Python Custom Skill For CSV Filtering

This code is a Python Custom Skill, for Azure Cognitive Search, based on Azure Functions for Python. Using the [Bing Search API](https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/), this skill will accept locations, public figures, and organizations, and will return Wikipedia descriptions for them.

This code implements url extraction. Change as you need!!

## Required steps

1. Follow [this](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python) tutorial.
1. Create one instance of the Content Moderator API in the [Azure Portal](https://ms.portal.azure.com/). You will need to add the access key to the py file of the step below.
1. Use the Python code below as your **__init__.py** file. Customize it with your storage account details, also with your csv file name and target column. As you can see below, my sample csv file target column name is **Term**. That helps the idea that this code will extract pre-defined terms from the documents content.
1. Don't forget to add **azure.functions** to your requirements.txt file.
1. Connect your published custom skill to your Cognitive Search Enrichment Pipeline. Plesae check the section below the code in this file. For more information, click [here](https://docs.microsoft.com/en-us/azure/search/cognitive-search-create-custom-skill-example#connect-to-your-pipeline).

## Python Code

The Python code for this skill is [here](./__init__.py). Please take a minute to read all comments witin the code, where many details and contraints are detailed.

## Add this skill to your Cogntive Search Enrichment Pipeline

Here, we're counting on the built-in entity recognition skill to be present in the skillset and to have enriched the document with the list of organizations. For reference, here's an entity extraction skill configuration that would be sufficient in generating the data we need.

```json
 {
            "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
            "name": "Bing Search API",
            "description": "Searching the built in organizations in the web",
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
            "targetName": "organizationsDescriptions"
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
            "text": "Flamengo"
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
            "text": "\\"
            Clube de Regatas do Flamengo, commonly referred to as Flamengo, is a Brazilian sports club based in Rio de Janeiro best known for their professional football team.\\
            ""
        }
    }]
}
```

