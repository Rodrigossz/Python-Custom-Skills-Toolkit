#This code opens the orgs.csv file in the same folder and finds those orgs in the input text
import logging
import azure.functions as func
import csv
import json
import re
import os

# Default Azure Functions Code - START
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

# Default Azure Functions Code - END

def run(json_data):

  # Get reference data - csv file
  __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
  myFile=os.path.join(__location__, 'terms.csv')
  myFile=os.path.normpath(myFile)

  with open (myFile,'r', encoding='latin-1') as csvList:
    myList = list(csv.reader(csvList))

    # Get the input data
    values = json.loads(json_data)['values']

    # Preparing output
    results = {}
    results["values"] = []
            
    # Process row by row
  
    for value in values:
      outputList=[]
      recordId = value['recordId']
      text = value['data']['text']

      # Adding and extra white spaces because I also add one for the terms
      text=' '+text+' '

      # Removing pontuaction, also because on the white spaces. 
      # A term followed by comma or other pontuaction would not be extracted because on the white spaces
      text = re.sub(r'[^\w\s]','',text)

      for term in myList:
          #Convert to string and add spaces to avoid things like 'Africa' been extracted from 'African'
          myStr=' '+str(term[0])+' '
          if text.lower().find(myStr.lower()) >= 0:
            #remove the white spaces
            myStr=myStr.strip()
            outputList.append(myStr)
      results["values"].append(
              {
              "recordId": recordId,
              "data": {
                  "text": outputList
                      }
              })
                    
    return json.dumps(results)


# sample_input_data = {
#   "values": 
#   [
#         {
#         "recordId": "0",
#         "data":
#           {
#              "text": "Today ASIA has better education levels. The African Union has approved a projec to improve the situation."
#           }
#         },
#       {
#         "recordId": "1",
#         "data":
#           {
#             "text": "ACCIDENT PREVENTION is very important."
#           }
     
#       }
#     ]
# }

# inputTest = json.dumps(sample_input_data)
# run(inputTest)
