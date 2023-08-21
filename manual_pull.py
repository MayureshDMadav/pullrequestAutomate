from backend.adhoc_request import apiRequestCallForAdhocMerchant
from backend.shopifydomainfetch import fetchShopifyDomain

# Manual Domain Update
def domainUpdateFunction(sheetNumber):
    fetchShopifyDomain(sheetNumber)


# Adhoc Sheet Data Processing    
def adhocSheetDataProcess():
    print("Updating Domain and removing Duplicates ===>")
    fetchShopifyDomain(2)
    print("Executing Rest API CAll ===>")
    apiRequestCallForAdhocMerchant(2)
    print("Adhoc Merchant Data Pull Completed ===>")
    
    
    
# Manually Call Adhoc Pull Request    
adhocSheetDataProcess()


# Manually Domain Updation Enter Sheet Number to process
# domainUpdateFunction(2)

