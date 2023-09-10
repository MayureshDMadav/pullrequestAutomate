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
def firsSheetRequestProcessing(sheetNumber):
    print("Updating Domain")
    fetchShopifyDomain(sheetNumber)
    print("Executing Rest API CAll  FirstSheet===>")
    apiRequestCallforNewMerchant(sheetNumber)
    print("Pushing Data to another sheet")
    pushDataFromFirstToSecond(1)
    print("Data have been processed Successfully")


# # Second Sheet Data Processing
def secondSheetRequestProcessing(sheetNumber):
    print("Removing Duplicates If any")
    dataFilter(sheetNumber)
    print("Updating Domain ===>")
    fetchShopifyDomain(sheetNumber)
    print("Executing Rest API CAll Second Sheet===>")
    apiRequestCallforWeeklyMerchant(sheetNumber)
    print("Successfully Update the details")

