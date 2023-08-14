from processheet.sheetprocess import everyDaySheetReading, everyDaySheetNetxDayWriting
from backend.apirequest import simplApiPullRequestCall
from backend.extrafunction import createRequestForPost
import json
import asyncio
from googleapiclient.errors import HttpError


# EVERY NEXT DAY PROCESSING FROM SHEET NAMED DAILY PULL
async def everyNextDay():
    response = everyDaySheetReading()
    responseArr = []
    for details in response:
        try:
            if (details):
                if details["status"] == 'Not Done' or details["status"] == 'NA' or details["status"] == ' ':
                    apiResponse = createRequestForPost(details)
                    response = await simplApiPullRequestCall(apiResponse)
                    print(response)
                    jsonParser = {details["merchant_name"]: response}
                    responseArr.append(jsonParser)
        except HttpError as err:
            print(err)
            return "No Sheet to connect"
    if responseArr:
        Final = everyDaySheetNetxDayWriting(responseArr)
        print("Final Triggered", Final)


asyncio.run(everyNextDay())
