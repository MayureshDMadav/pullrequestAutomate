import schedule
import time
from backend.shopifydomainfetch import fetchShopifyDomain
from processheet.sheetprocessor import pushDataFromFirstToSecond, dataFilter ,pushDataFromSalesForceToFirst
from backend.new_merchant_address import apiRequestCallforNewMerchant
from backend.weekly_data_request import apiRequestCallforWeeklyMerchant
from backend.failed_scnerio import failedScenarioApiCall


# SCHEDULAR FUNCTIONS

# Rest API CALL For New Merchant
def firsSheetRequestProcess():
    print("Updating Domain and removing Duplicates ===>")
    fetchShopifyDomain(0)
    print("Executing Rest API CAll  FirstSheet===>")
    apiRequestCallforNewMerchant(0)
    print("Checking Failed Responses and reinitiating API Request")
    failedScenarioApiCall(0)
    print("ReAttempt Ended")
    pushDataFromFirstToSecond(1)
    dataFilter(1)
    print("Data have been processed Successfully")


# Second Sheet Data Processing
def secondSheetRequestProcess():
    print("Updating Domain and removing Duplicates ===>")
    fetchShopifyDomain(1)
    print("Executing Rest API CAll Second Sheet===>")
    apiRequestCallforWeeklyMerchant(1)
    print("Checking Failed Responses and re-initiating API Request")
    failedScenarioApiCall(1)
    print("ReAttempt Ended")
    time.sleep(1)
    print("Successfully Update the details")


# Weekly schedular
schedule.every().thursday.at('17:00').do(secondSheetRequestProcess)


# Daily Schedular
schedule.every().tuesday.at('09:00').do(firsSheetRequestProcess)
schedule.every().wednesday.at('09:00').do(firsSheetRequestProcess)
schedule.every().thursday.at('09:00').do(firsSheetRequestProcess)
schedule.every().friday.at('09:00').do(firsSheetRequestProcess)
schedule.every().saturday.at('09:00').do(firsSheetRequestProcess)


# Push Data From SalesForce Sheet to New Merchant Sheet
schedule.every().monday.at('09:00').do(pushDataFromSalesForceToFirst(3))
schedule.every().tuesday.at('09:00').do(pushDataFromSalesForceToFirst(3))
schedule.every().wednesday.at('09:00').do(pushDataFromSalesForceToFirst(3))
schedule.every().thursday.at('09:00').do(pushDataFromSalesForceToFirst(3))
schedule.every().friday.at('09:00').do(pushDataFromSalesForceToFirst(3))
schedule.every().saturday.at('09:00').do(pushDataFromSalesForceToFirst(3))



while True:
    schedule.run_pending()
    time.sleep(1)
