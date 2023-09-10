import schedule
import time
# from backend.shopifydomainfetch import fetchShopifyDomain
# from processheet.sheetprocessor import pushDataFromSalesForceToFirst
from manual_pull import firsSheetRequestProcessing,secondSheetRequestProcessing


# SCHEDULAR FUNCTIONS

# Rest API CALL For New Merchant
def firsSheetRequestProcess():
    firsSheetRequestProcessing(0)


# Second Sheet Data Processing
def secondSheetRequestProcess():
    secondSheetRequestProcessing(1)

# Weekly schedular
schedule.every().thursday.at('17:00').do(secondSheetRequestProcess)


# Daily Schedular
schedule.every().tuesday.at('09:00').do(firsSheetRequestProcess)
schedule.every().wednesday.at('09:00').do(firsSheetRequestProcess)
schedule.every().thursday.at('09:00').do(firsSheetRequestProcess)
schedule.every().friday.at('09:00').do(firsSheetRequestProcess)
schedule.every().saturday.at('09:00').do(firsSheetRequestProcess)


# def pushDataFromSalesForcetoFirstSheet():
#     pushDataFromSalesForceToFirst(3)


# Push Data From SalesForce Sheet to New Merchant Sheet
# schedule.every().monday.at('09:00').do(pushDataFromSalesForcetoFirstSheet)
# schedule.every().tuesday.at('09:00').do(pushDataFromSalesForcetoFirstSheet)
# schedule.every().wednesday.at('09:00').do(pushDataFromSalesForcetoFirstSheet)
# schedule.every().thursday.at('09:00').do(pushDataFromSalesForcetoFirstSheet)
# schedule.every().friday.at('09:00').do(pushDataFromSalesForcetoFirstSheet)
# schedule.every().saturday.at('09:00').do(pushDataFromSalesForcetoFirstSheet)


# firsSheetRequestProcess()

# while True:
#     schedule.run_pending()
#     time.sleep(1)

firsSheetRequestProcess()