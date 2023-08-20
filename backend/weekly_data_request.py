import sys
import os

current_directory = os.getcwd()
parent_directory = os.path.dirname(os.path.abspath(current_directory))
sys.path.append(parent_directory)

from processheet.sheetprocessor import dataFilter,writeApiCallDataForWeek
from backend.extrafunction import createRequestForPost
from backend.apirequest import testApiCall

def apiRequestCallforWeeklyMerchant(sheetNumber):
    try:
        dataFromSheet = dataFilter(sheetNumber)
        if dataFromSheet:            
            for index , data in enumerate(dataFromSheet):
                if  data.get('shopify_domain',""):                
                    domainUrl = data.get('shopify_domain',"")
                    apiRequestForPost = createRequestForPost(domainUrl)
                    response = testApiCall(apiRequestForPost)
                    if(response == True):
                        data = {"merchant_name":data.get('merchant_name',"") ,"shopify_domain": data.get('shopify_domain',""),  "status":"Done"}
                        writeApiCallDataForWeek(data,1)
                    else:
                        data = {"merchant_name":data.get('merchant_name',"") ,"shopify_domain": data.get('shopify_domain',""), "status":"Failed"}
                        writeApiCallDataForWeek(data,1)
    except:
        print("Issue in weekly request Merchant")






