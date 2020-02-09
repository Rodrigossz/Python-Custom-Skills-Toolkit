import azure.functions as func
import json
import re
import http.client, urllib.request, urllib.parse, urllib.error, base64

def transform_value(value):
    try:
        recordId = value['recordId']
    except AssertionError  as error:
        return None

    # Validate the inputs
    try:         
        assert ('data' in value), "'data' field is required."
        data = value['data']        
        assert ('text' in data), "'text' field is required in 'data' object."
    except AssertionError  as error:
        return (
            {
            "recordId": recordId,
            "data":{},
            "errors": [ { "message": "Error:" + error.args[0] }   ]
            })

    # Getting the input text and converting to list
    myString = value['data']['text']

    # Request headers - ACTION REQUIRED!!!
    # REPLACE THE STRING BELOW WITH YOUR KEY!!
    subscriptionKey = '4e992f1885964439ab56770277e3752c'

    # Other Params
    host = 'api.cognitive.microsoft.com'
    path = '/bing/v7.0/entities'
    mkt = 'en-US'
    query = myString
    params = '?mkt=' + mkt + '&q=' + urllib.parse.quote (query)

    def get_suggestions ():
        headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
        conn = http.client.HTTPSConnection (host)
        conn.request ("GET", path + params, None, headers)
        response = conn.getresponse ()
        return response.read()

    result = get_suggestions ()
    myString =  (json.dumps(json.loads(result), indent=4))
    myString = str(myString)
    print(myString)



myInputTest = {
    "recordId": "0",
    "data": {
        "text": ["Flamengo"]
    }
}

myInputTest = json.dumps(myInputTest)
transform_value (myInputTest)
