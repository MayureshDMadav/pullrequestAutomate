import schedule
import time
# from backend.shopifydomainfetch import fetchShopifyDomain
from processheet.sheetprocessor import pusDataFromSalesForceToFirst
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
schedule.every().tuesday.at('11:00').do(firsSheetRequestProcess)
schedule.every().wednesday.at('11:00').do(firsSheetRequestProcess)
schedule.every().thursday.at('11:00').do(firsSheetRequestProcess)
schedule.every().friday.at('11:00').do(firsSheetRequestProcess)
schedule.every().saturday.at('11:00').do(firsSheetRequestProcess)


# def pushDataFromSalesForcetoFirstSheet():
#     pushDataFromSalesForceToFirst(3)


def pusDataFromSalesForce():
    pusDataFromSalesForceToFirst(0)

# Push Data From SalesForce Sheet to New Merchant Sheet
schedule.every().monday.at('20:00').do(pusDataFromSalesForce)
schedule.every().tuesday.at('20:00').do(pusDataFromSalesForce)
schedule.every().wednesday.at('20:00').do(pusDataFromSalesForce)
schedule.every().thursday.at('20:00').do(pusDataFromSalesForce)
schedule.every().friday.at('20:00').do(pusDataFromSalesForce)
schedule.every().saturday.at('20:00').do(pusDataFromSalesForce)


# firsSheetRequestProcess()

while True:
    schedule.run_pending()
    time.sleep(1)

