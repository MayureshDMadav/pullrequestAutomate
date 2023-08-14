from processheet.sheetprocess import everyDaySheetReading, everyDaySheetNetxDayWriting, everyWeekSheetReading, everyNextWeekSheetWriting, adhocDataInsert, adhocRequestReading
from backend.apirequest import simplApiPullRequestCall
from backend.extrafunction import createRequestForPost
from googleapiclient.errors import HttpError


# EVERY NEXT DAY PROCESSING FROM SHEET NAMED DAILY PULL

async def everyNextDay():
    try:
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
                    else:
                        print("status not found")
            except HttpError as err:
                print(err)
                return "No Sheet to connect"
        if responseArr:
            Final = everyDaySheetNetxDayWriting(responseArr)
            if (Final):
                print("Data successfully Inserted to the sheet")
            else:
                print("Data insertion failed")
    except Exception as e:
        print(e)
        print("every next Day function Failed !!")


# EVERY NEXT WEEK  PROCESSING FROM SHEET NAMED DAILY PULL


async def everyWeekDataProcess():
    try:
        response = everyWeekSheetReading()
        responseArr = []
        for details in response:
            try:
                if (details):
                    apiResponse = createRequestForPost(details)
                    response = await simplApiPullRequestCall(apiResponse)
                    jsonParser = {details["merchant_name"]: response}
                    responseArr.append(jsonParser)
                else:
                    return False
            except HttpError as err:
                print(err)
                return "No Sheet to connect"
        if responseArr:
            Final = everyNextWeekSheetWriting(responseArr)
            if (Final):
                print("Data successfully Inserted to the sheet")
            else:
                print("Data insertion failed")
    except Exception as e:
        print(e)
        print("every Week Data function Failed !!")


# ADHOC REQUES PROCESSING


async def adhocRequestProcess():
    try:
        response = adhocRequestReading()
        responseArr = []
        for details in response:
            try:
                if (details):
                    apiResponse = createRequestForPost(details)
                    response = await simplApiPullRequestCall(apiResponse)
                    jsonParser = {details["merchant_name"]: response}
                    responseArr.append(jsonParser)
                else:
                    return False
            except HttpError as err:
                print(err)
                return "No Sheet to connect"
        if responseArr:
            Final = adhocDataInsert(responseArr)
            if (Final):
                print("Data successfully Inserted to the sheet")
                return True
            else:
                print("Data insertion failed")
                return False
    except Exception as e:
        print(e)
        print("Adhoc Request Failed !!!")
