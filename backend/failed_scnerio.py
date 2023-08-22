import sys
import os

current_directory = os.getcwd()
parent_directory = os.path.dirname(os.path.abspath(current_directory))
sys.path.append(parent_directory)


from processheet.sheetprocessor import dataFilter,failedScenarioUpdateApiCall
from backend.extrafunction import createRequestForPost
from backend.apirequest import simplApiPullRequestCall


def failedScenarioApiCall(sheetNumber):
    try:
        dataFromSheet = dataFilter(sheetNumber)
        if dataFromSheet:            
            for index , data in enumerate(dataFromSheet):
                if data.get('status',"") == 'Failed' or data.get('status',"") == 'Re-attempted Failed' and data.get('shopify_domain',""):        
                    domainUrl = data.get('shopify_domain',"")  
                    apiRequestForPost = createRequestForPost(domainUrl)
                    response = simplApiPullRequestCall(apiRequestForPost)
                    if(response == True):
                        data = {"merchant_name":data.get('merchant_name',"") ,"shopify_domain": data.get('shopify_domain',""),  "status":"Re-attempted Success"}
                        failedScenarioUpdateApiCall(data,sheetNumber)
                    else:
                        data = {"merchant_name":data.get('merchant_name',"") ,"shopify_domain": data.get('shopify_domain',""), "status":"Re-attempted Failed"}
                        failedScenarioUpdateApiCall(data,sheetNumber)
            print("Skipping Process as No Data Found on Failed Scenario !!")
    except Exception as e:
        print(e)
        print("Response")



