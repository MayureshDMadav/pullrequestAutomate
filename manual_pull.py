from backend.adhoc_request import apiRequestCallForAdhocMerchant
from backend.shopifydomainfetch import fetchShopifyDomain
from backend.failed_scnerio import failedScenarioApiCall
from backend.shopifydomainfetch import fetchShopifyDomain
from processheet.sheetprocessor import pushDataFromFirstToSecond, dataFilter
from backend.new_merchant_address import apiRequestCallforNewMerchant
from backend.weekly_data_request import apiRequestCallforWeeklyMerchant
from backend.failed_scnerio import failedScenarioApiCall


# Manual Domain Update
# def domainUpdateFunction(sheetNumber):
#     fetchShopifyDomain(sheetNumber)


# Adhoc Sheet Data Processing    
# def adhocSheetDataProcess():
#     print("Updating Domain and removing Duplicates ===>")
#     fetchShopifyDomain(2)
#     print("Executing Rest API CAll For ADHOC Request ===>")
#     apiRequestCallForAdhocMerchant(2)
#     print("Adhoc Merchant Data Pull Completed ===>")
    
# Failed Scenario Request Processing
# failedScenarioApiCall(0)
    
# # Manually Call Adhoc Pull Request    
# # adhocSheetDataProcess()


# # Manually Domain Updation Enter Sheet Number to process
# # domainUpdateFunction(2)


# # Rest API CALL For New Merchant
# def firsSheetRequestProcess():
#     print("Updating Domain and removing Duplicates ===>")
#     fetchShopifyDomain(0)
#     print("Executing Rest API CAll  FirstSheet===>")
#     apiRequestCallforNewMerchant(0)
#     print("Checking Failed Responses and reinitiating API Request")
#     failedScenarioApiCall(0)
#     print("ReAttempt Ended")
#     pushDataFromFirstToSecond(1)
#     dataFilter(1)
#     print("Data have been processed Successfully")


# # Second Sheet Data Processing
# def secondSheetRequestProcess():
#     print("Updating Domain and removing Duplicates ===>")
#     fetchShopifyDomain(1)
#     print("Executing Rest API CAll Second Sheet===>")
#     apiRequestCallforWeeklyMerchant(1)
#     print("Checking Failed Responses and re-initiating API Request")
#     failedScenarioApiCall(1)
#     print("ReAttempt Ended")
#     time.sleep(1)
#     print("Successfully Update the details")

