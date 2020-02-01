# Azure Cognitive Search Python Custom Skill For Strings Concatenation

This code is a Python Custom Skill, for Azure Cognitive Search, based on Azure Functions for Python. It merges 2 strings in a third one, useful when you want to concatenate, within an Enrichment Pipeline, the file name or path with the content. This skill is indicated for scenarios when the file name or path have dates, organizations, names, or key phrases. 

Until January 2020, you can't do this merge usint the Built In Merge Skill since you won't have the required offistes. I just suggested this feature as a built in capability. For now, this code is the alternative.

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

Use the JSON input below to test your function. Get familiar with the code behavior in the different situations. 

This test text is a tribute to the most popular football club in the world, [Flamengo](https://en.wikipedia.org/wiki/Clube_de_Regatas_do_Flamengo), from Rio de Janeiro. It was founded in 1895 and has over 45 million fans in Brazil alone. The team was [champion](https://www.youtube.com/watch?time_continue=11&v=371FOyquzno) in its two most important matches of 2019, the Brazilian championship and the Copa Libertadores of America.

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
            "string1": "Flamengo_Libertadores_2019.jpg"
            }
      },
        {
        "recordId": "2",
        "data":
           {
            "string1": "Flamengo_Libertadores_2019.jpg",
            "string2": "",

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
            "text": "Flamengo is the new champion"
        }
    }, {
        "recordId": "1",
        "data": "{}",
        "errors": [{
            "message": "Error:\'string2\' field is required in \'data\' object."
        }]
    }, {
        "recordId": "2",
        "data": {
            "text": "Flamengo_Libertadores_2019.jpg "
        }
    }]
}
```

