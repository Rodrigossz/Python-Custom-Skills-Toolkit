# This code removes special characters like \t and \n from strings

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
      # Getting the document text (content + OCR(?) + any other text been analyzed within your enrichment pipeline)
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
                    
    return json.dumps(results)


sample_input_data = {
    "values": [
      {
        "recordId": "0",
        "data":
           {
             "text": "\t\n\tUnited Nations\n\t\n\tE/RES/2018/27\n\n\t [image: ]\n\tEconomic and Social Council\n\t\n\tDistr.: General\n7 August 2018\n\n\n\n\n\tE/RES/2018/27\n\tReport of the Committee for Development Policy on its twentieth session\n\n\n\n\tReport of the Committee for Development Policy on its twentieth session\n\tE/RES/2018/27\n\n\n\n\n\t[image: https://undocs.org/m2/QRCode2.ashx?DS=E/RES/2018/27&Size =1&Lang = E]18-12682 (E)    150818    \n*1812682*\n\t[image: ]\n\n\n\n\t18-12682\n\t2/3\n\n\n\n\t3/3\n\t18-12682\n\n\n\n2018 session\nAgenda item 18 (a)\n\n\n\n\t\tResolution adopted by the Economic and Social Council on 24 July 2018\n\n\n\t\t[on a proposal considered in plenary meeting (E/2018/L.22)]\n\n\n\t2018/27.\tReport of the Committee for Development Policy on its twentieth session\n\n\n\tThe Economic and Social Council,\n\tRecalling General Assembly resolutions 59/209 of 20 December 2004 and 67/221 of 21 December 2012, both on a smooth transition strategy for countries graduating from the category of least developed countries, \n\tRecalling also that, in its resolution 59/209, the General Assembly decided that graduation from the least developed country category would become effective three years after the date on which the Assembly had taken note of the recommendation of the Committee for Development Policy to graduate a country from the category and that, during the three-year period, the country would remain on the list of least developed countries and "
           }
      }]
}

inputTest = json.dumps(sample_input_data)
run(inputTest)
