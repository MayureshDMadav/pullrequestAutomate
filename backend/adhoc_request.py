from processheet.sheetprocessor import adhocSheetDataReading, writeApiCallDataForAdhoc
from backend.apirequest import simplApiPullRequestCall
from backend.extrafunction import createRequestForPostAdhoc
import sys
import os

current_directory = os.getcwd()
parent_directory = os.path.dirname(os.path.abspath(current_directory))
sys.path.append(parent_directory)


def apiRequestCallForAdhocMerchant(sheetNumber):
    try:
        dataFromSheet = adhocSheetDataReading(sheetNumber)
        if dataFromSheet:
            for index, data in enumerate(dataFromSheet):
                if data.get('shopify_domain', "") and data.get('status', "") == 'Not Done':
                    domainUrl = data.get('shopify_domain', "")
                    startTime = data.get('startTime',"")
                    apiRequestForPost = createRequestForPostAdhoc(startTime,domainUrl)
                    response = simplApiPullRequestCall(apiRequestForPost)
                    if (response == True):
                        data = {"merchant_name": data.get('merchant_name', ""), "shopify_domain": data.get(
                            'shopify_domain', ""),  "status": "Done"}
                        writeApiCallDataForAdhoc(data, 2)
                    else:
                        data = {"merchant_name": data.get('merchant_name', ""), "shopify_domain": data.get(
                            'shopify_domain', ""), "status": "Failed"}
                        writeApiCallDataForAdhoc(data, 2)
    except:
        print("Issue in Adhoc request Merchant")


