# This code is an Azure Cognitive Search Python Custom Skill. It will return the FIRST date of the input. 
#
#
# CHANGE THIS CODE AS YOU NEED!!!
#
#
# For production environments, add logging and error tests.
# The output format is YYYY-MM-DD.
#
# The datafinder Characteristics:
# 1) If the year is detected without month or day, it will be returned with today's month and day.
# 2) If month and date are detected without year, it will return the date with today's year.
# 3) The datafinder library will deal with empty stings and we will handle the outpout format
# 
# For more details about datefinder: https://datefinder.readthedocs.io/en/latest/

import logging
import azure.functions as func
import re
import datefinder
import json
import datetime

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
      
      try:
        myString = value['data']['text']
      except ValueError:
        pass

      if myString:
        # Converting to String and Removing Special Characters 
        myString=str(myString)
        myString = re.sub(r'\t',' ',myString)
        myString = re.sub(r'\n',' ',myString)
        myString = re.sub(r'  ',' ',myString)

        # Getting the dates into an empty Generator
        matches = datefinder.find_dates(myString)

        #First Date only
        for match in matches:
          myDate = match
          # Convert to string
          myDateString = str(myDate)
          break

        # Remove time for the date found
        # Add extra validations if you need
        if len(myDateString) > 1:
          myDateString = myDateString[0:10]
        else:
          myDateString = ''

        # Output
        recordId = value['recordId']
        results["values"].append(
              {
              "recordId": recordId,
              "data": {
                  "text": myDateString
                      }
              })
                    
    return json.dumps(results)

# sample_input_data = {
#     "values": [
#       {
#         "recordId": "0",
#         "data":
#            {
#              "text": "\t\n\tUnited Nations\n\t\n\tE/RES/2018/27\n\n\t [image: ]\n\tEconomic and Social Council\n\t\n\tDistr.: General\n7 August 2018\n\n\n\n\n\tE/RES/2018/27\n\tReport of the Committee for Development Policy on its twentieth session\n\n\n\n\tReport of the Committee for Development Policy on its twentieth session\n\tE/RES/2018/27\n\n\n\n\n\t[image: https://undocs.org/m2/QRCode2.ashx?DS=E/RES/2018/27&Size =1&Lang = E]18-12682 (E)    150818    \n*1812682*\n\t[image: ]\n\n\n\n\t18-12682\n\t2/3\n\n\n\n\t3/3\n\t18-12682\n\n\n\n2018 session\nAgenda item 18 (a)\n\n\n\n\t\tResolution adopted by the Economic and Social Council on 24 July 2018\n\n\n\t\t[on a proposal considered in plenary meeting (E/2018/L.22)]\n\n\n\t2018/27.\tReport of the Committee for Development Policy on its twentieth session\n\n\n\tThe Economic and Social Council,\n\tRecalling General Assembly resolutions 59/209 of 20 December 2004 and 67/221 of 21 December 2012, both on a smooth transition strategy for countries graduating from the category of least developed countries, \n\tRecalling also that, in its resolution 59/209, the General Assembly decided that graduation from the least developed country category would become effective three years after the date on which the Assembly had taken note of the recommendation of the Committee for Development Policy to graduate a country from the category and that, during the three-year period, the country would remain on the list of least developed countries and maintain the advantages associated with membership on that list, and that, in its resolution 67/221, the Assembly decided to take note of the decisions of the Economic and Social Council regarding the graduation of countries from and the inclusion in the list of least developed countries at the first session of the Assembly following the adoption of such decisions by the Council,\n[bookmark: _GoBack]\tRecalling further General Assembly resolution 65/280 of 17 June 2011, by which the Assembly endorsed the Istanbul Declaration[footnoteRef:1] and the Programme of Action for the Least Developed Countries for the Decade 2011–2020,[footnoteRef:2] whose overarching goal is to overcome the structural challenges faced by the least developed countries in order to eradicate poverty, achieve internationally agreed development goals and enable graduation from the least developed country category, and, guided by that overarching goal, focuses the national policies of least developed countries and international support measures during the decade on the five specific objectives described in the Programme of Action, with the aim of enabling half the number of least developed countries to meet the criteria for graduation by 2020, [1: \t \tReport of the Fourth United Nations Conference on the Least Developed Countries, Istanbul, Turkey, 9–13 May 2011 (A/CONF.219/7), chap. I.]  [2: \t \tIbid.,"
#            }
#       },
#             {
#         "recordId": "1",
#         "data":
#            {
#              "text": 'november 23 2015'
#       },
#             }
#       ]
# }

# inputTest = json.dumps(sample_input_data)
# run(inputTest)
