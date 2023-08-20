import sys
import os

current_directory = os.getcwd()
parent_directory = os.path.dirname(os.path.abspath(current_directory))
sys.path.append(parent_directory)

from processheet.sheetprocessor import dataFilter,writeApiCallData
from backend.extrafunction import createRequestForPost
from backend.apirequest import testApiCall

def apiRequestCallforNewMerchant(sheetNumber):
    try:
        dataFromSheet = dataFilter(sheetNumber)
        if dataFromSheet:            
            for index , data in enumerate(dataFromSheet):
                if data.get('status',"") == 'Not Done' and data.get('shopify_domain',""):                
                    domainUrl = data.get('shopify_domain',"")
                    apiRequestForPost = createRequestForPost(domainUrl)
                    response = testApiCall(apiRequestForPost)
                    if(response == True):
                        data = {"merchant_name":data.get('merchant_name',"") ,"shopify_domain": data.get('shopify_domain',""),  "status":"Done"}
                        writeApiCallData(data,0)
                    else:
                        data = {"merchant_name":data.get('merchant_name',"") ,"shopify_domain": data.get('shopify_domain',""), "status":"Failed"}
                        writeApiCallData(data,0)
    except:
        print("Response")





