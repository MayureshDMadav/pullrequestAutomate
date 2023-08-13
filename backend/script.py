from sheetProcess.sheetprocess import sheetDataProcessReadOnly, writeOnSheet
from backend.apirequest import requestTriggered
import json
from googleapiclient.errors import HttpError


def main():
    response = sheetDataProcessReadOnly()
    responseArr = []
    for details in response:
        try:
            if (details):
                if details["status"] == 'Not Done' or details["status"] == 'NA' or details["status"] == ' ':
                    apiResponse = requestTriggered(details)
                    jsonData = json.loads(apiResponse)
                    jsonParser = {details["merchant_name"]: jsonData["status"]}
                    responseArr.append(jsonParser)
        except HttpError as err:
            print(err)
            return "No Sheet to connect"
    if responseArr:
        Final = writeOnSheet(responseArr)
        print(Final)


main()
