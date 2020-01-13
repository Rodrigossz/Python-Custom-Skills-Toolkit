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
        # Special Characters Removal since we want to help the Text Analytics API to find key phrases, etc.
        # If your files have dates or time in the name, change this code to process it.
        string1 = re.sub('[^A-Za-z0-9]+', ' ',value['data']['string1']) 
        string2 = re.sub('[^A-Za-z0-9]+', ' ',value['data']['string2'])
        mergedStrings = " "+ string1 + " "+ string2 + " "
        recordId = value['recordId']
        results["values"].append(
                {
                "recordId": recordId,
                "data": {
                    "text": mergedStrings
                        }
                })
                    
    return json.dumps(results)
