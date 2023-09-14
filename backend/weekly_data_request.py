import sys
import os

current_directory = os.getcwd()
parent_directory = os.path.dirname(os.path.abspath(current_directory))
sys.path.append(parent_directory)

from processheet.sheetprocessor import fetchSheetData,writeApiCallDataForWeek
from backend.extrafunction import createRequestForPost
from backend.apirequest import simplApiPullRequestCall,testApiCall

def apiRequestCallforWeeklyMerchant(sheetNumber):
    try:
        dataFromSheet = fetchSheetData(sheetNumber)
        if dataFromSheet:            
            for index , data in enumerate(dataFromSheet):
                if  data.get('shopify_domain',""):                
                    domainUrl = data.get('shopify_domain',"")
                    apiRequestForPost = createRequestForPost(domainUrl)
                    response = simplApiPullRequestCall(apiRequestForPost)
                    if(response == True):
                        data = {"merchant_name":data.get('merchant_name',"") ,"shopify_domain": data.get('shopify_domain',""),  "status":"Done"}
                        writeApiCallDataForWeek(data,sheetNumber)
                    else:
                        data = {"merchant_name":data.get('merchant_name',"") ,"shopify_domain": data.get('shopify_domain',""), "status":"Failed"}
                        writeApiCallDataForWeek(data,sheetNumber)
    except Exception as e:
        print(e)
        print("Issue in weekly request Merchant")





