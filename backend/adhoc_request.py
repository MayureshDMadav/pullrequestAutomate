import sys
import os

current_directory = os.getcwd()
parent_directory = os.path.dirname(os.path.abspath(current_directory))
sys.path.append(parent_directory)
from backend.apirequest import simplApiPullRequestCall,testApiCall
from processheet.sheetprocessor import adhocSheetDataReading, writeApiCallDataForAdhoc
from backend.extrafunction import createRequestForPostAdhoc

def apiRequestCallForAdhocMerchant(sheetNumber):
    try:
        dataFromSheet = adhocSheetDataReading(sheetNumber)
        if dataFromSheet:
            for index, data in enumerate(dataFromSheet):
                if data.get('shopify_domain', "") and data.get('status', "") == 'Not Done':
                    domainUrl = data.get('shopify_domain', "")
                    startTime = data.get('start_time',"")
                    endTime = data.get("end_time","")
                    apiRequestForPost = createRequestForPostAdhoc(startTime,endTime,domainUrl)
                    response = simplApiPullRequestCall(apiRequestForPost)
                    if (response == True):
                        data = {"merchant_name": data.get('merchant_name', ""), "shopify_domain": data.get(
                            'shopify_domain', ""),  "status": "Done"}
                        writeApiCallDataForAdhoc(data, 2)
                    else:
                        data = {"merchant_name": data.get('merchant_name', ""), "shopify_domain": data.get(
                            'shopify_domain', ""), "status": "Failed"}
                        writeApiCallDataForAdhoc(data, 2)
    except Exception as e:
        print("Issue in Adhoc request Merchant")
        print(e)

