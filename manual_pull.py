from backend.adhoc_request import apiRequestCallForAdhocMerchant
from backend.shopifydomainfetch import fetchShopifyDomain
from backend.failed_scnerio import failedScenarioApiCall

# Manual Domain Update
def domainUpdateFunction(sheetNumber):
    fetchShopifyDomain(sheetNumber)


# Adhoc Sheet Data Processing    
def adhocSheetDataProcess():
    print("Updating Domain and removing Duplicates ===>")
    fetchShopifyDomain(2)
    print("Executing Rest API CAll For ADHOC Request ===>")
    apiRequestCallForAdhocMerchant(2)
    print("Adhoc Merchant Data Pull Completed ===>")
    
# Failed Scenario Request Processing
failedScenarioApiCall(0)
    
# Manually Call Adhoc Pull Request    
# adhocSheetDataProcess()


# Manually Domain Updation Enter Sheet Number to process
# domainUpdateFunction(2)

