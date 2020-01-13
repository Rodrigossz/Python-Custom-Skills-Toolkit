# Pyhton-Custom-Skills-for-Azure-Cognitive-Search
This repo is a collection of useful functions to be deployed as custom skills for Azure Cognitive Search. The skills can be used as **templates or starting points** for your own custom skills, or they can be deployed and used as they are if they happen to meet your requirements. For enterprise/production/corporate environments, I suggest you change the code so that it complies with the performance and security requirements of your project, or your company. 

All code was written for Azure Functions in Python 3.7, to address specific projects requirements. Please read all the comments of the code to understand what was done, including limitations and restrictions. Again, adapt the code for your own requirements and needs.

## What is Azure Cognitive Search
Azure Cognitive Search (formerly known as "Azure Search") is a search-as-a-service cloud solution that gives developers APIs and tools for adding a rich search experience over private, heterogeneous content in web, mobile, and enterprise applications. Your code or a tool invokes data ingestion (indexing) to create and load an index. Optionally, you can add cognitive skills to apply AI processes during indexing. Doing so can add new information and structures useful for search and other scenarios.

To learn more about Azure Cognitive Search, click [here](https://docs.microsoft.com/en-us/azure/search/search-what-is-azure-search). 

## What is Azure Cognitive Search Custom Skill
The Custom Web API skill allows you to extend AI enrichment by calling out to a Web API endpoint providing custom operations. Similar to built-in skills, a Custom Web API skill has inputs and outputs. Depending on the inputs, your Web API receives a JSON payload when the indexer runs, and outputs a JSON payload as a response, along with a success status code. The response is expected to have the outputs specified by your custom skill. Any other response is considered an error and no enrichments are performed. 

To learn more about Custom Skills, click [here](https://docs.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-interface).

## What is Azure Functions
It is an event-driven serverless compute platform that can also solve complex orchestration problems. Build and debug locally without additional setup, deploy and operate at scale in the cloud, and integrate services using triggers and bindings.

To learn more about Azure Functions, click [here](https://azure.microsoft.com/en-us/services/functions/)

## Reference Architecture
The image below gives you an example on how all of these services can work integrated into a Knowledge Mining solution.

![Reference Architecture](./images/reference.JPG)

I know how a customized slide can help POCs, Demos, Design Sessions, etc. If you want to customize this diagram, just use the provided ppt file.

## Suggested IDEs

Python allows you to use multiple IDEs like [Azure Notebooks](https://notebooks.azure.com/), [Azure Notebook VMs](https://azure.microsoft.com/en-us/blog/three-things-to-know-about-azure-machine-learning-notebook-vm/), [Visual Studio](https://visualstudio.microsoft.com/), etc.

My favorite IDE for this kind of project is [Visual Studio Code](https://code.visualstudio.com/). Some reasons why:

+ [Azure Functions extention](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
+ [Python extention](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
+ [REST API extention](https://marketplace.visualstudio.com/items?itemName=mkloubert.vs-rest-api)
+ [Great  Tutorial](https://code.visualstudio.com/docs/languages/python)
+ [Locally integrated features: Dvelopment, tests, and deployment to Azure](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-vs-code)

## Code - The Skills

Skill | When to Use
:---:|:---
Dates Extractor | Extracts dates from string. Differentiates itself from the [Entity Extraction built-in skill](https://docs.microsoft.com/en-us/azure/search/cognitive-search-skill-entity-recognition) by generating dates in yyyy-mm-dd HH:MM:SS format. 
Strings Merger | Merges 2 strings. Differentiates itself from the [Text Merger built-in skill](https://docs.microsoft.com/en-us/azure/search/cognitive-search-skill-textmerger) by allowing you to merge any 2 strings, not only the content with the OCR text extracted from images.
Strings Cleaner | Removes special characters from strings, returning a string clean of those values.
CSV Filtering | Removes the csv file values from the input, returning a string clean of those values.
CSV Lookup | Extracts the csv file values that were found in the input string, returning an array of strings.

## C# Custom Skills from the Azure Cognitive Search Product Team 
I work for [Microsoft AI Customer Engineering Team](ka.ms/ace-blog). For "official" Azure Search click-to-deploy C# Custom skills, created by the Azure Cognitive Search Team, use the [Azure Search Power Skills repo](https://github.com/Azure-Samples/azure-search-power-skills).

## Collaboration
We also invite you to contribute your own work by submitting a pull request.

## About Me
My name is Rodrigo Souza and I work for Microsoft since 2017. For now my roles within the company were Data Solutions Architect, AI Instructor, and Applied Data Scientist. Some key links about me:

+ [LinkedIn](https://www.linkedin.com/in/rodrigossz/)
+ [Visual CV](https://github.com/Rodrigossz/CV)
+ [How I did become a Data Scientist](https://www.linkedin.com/pulse/how-did-i-become-data-scientist-rodrigo-souza/)
+ [Using data and creativity to overcome challenges](https://www.linkedin.com/pulse/using-data-creativity-overcome-challenges-rodrigo-souza/)
+ [DBAs in the Cloud & AI Age](https://www.linkedin.com/pulse/dbas-cloud-ai-age-rodrigo-souza/)