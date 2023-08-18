import os.path
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import datetime


load_dotenv()

current_dir = os.path.dirname(__file__)
token_path = os.path.join(current_dir, 'keys.json')

creds = None


def validateSheet():
    global creds
    if os.path.exists(token_path):
        creds = service_account.Credentials.from_service_account_file(
            token_path, scopes=[os.getenv("SCOPES")])
    else:
        print("Data file not found")


def fetchSheetData(sheetNumber):
    validateSheet()
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet = sheet.get(spreadsheetId=os.getenv(
            "SAMPLE_SPREADSHEET_ID")).execute()
        sheet_properties = spreadsheet.get(
            "sheets", [])[sheetNumber].get("properties", {})
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties.get(
            "gridProperties", {}).get("rowCount", 0)
        last_col = sheet_properties.get(
            "gridProperties", {}).get("columnCount", 0)

        auto_range = f"{sheet_title}!A1:{chr(64 + last_col)}{last_row}"

        result = sheet.values().get(spreadsheetId=os.getenv("SAMPLE_SPREADSHEET_ID"),
                                    range=auto_range).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        if len(values) > 0:
            values.pop(0)

        merchant_data = []
        for data in values:
            merchant_data.append(data)

        if len(merchant_data) > 0:
            merchant_data.pop(0)

        global merchant_list
        merchant_list = []
        for merchant_name in merchant_data:
            if len(merchant_name[0]) > 1 and len(merchant_name[1]) > 1:
                sheetData = {
                    "merchant_name": merchant_name[0],
                    "merchant_url": merchant_name[1],
                    "shopify_domain": merchant_name[2],
                    "status": merchant_name[3]
                }
                merchant_list.append(sheetData)

        return merchant_list

    except HttpError as err:
        print(err)
        merchant_list.append({"status": False})
        return merchant_list


def writeShopifyDomain(data, sheetNumber):
    validateSheet()
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        spreadsheet = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = spreadsheet.get(
            "sheets", [])[sheetNumber].get("properties", "")
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties.get(
            "gridProperties", {}).get("rowCount", 0)
        
        for row,merchant_name in enumerate(merchant_list):
            if len(merchant_name['shopify_domain']) < 1:
                if data:
                    if data["merchant_name"] == merchant_name["merchant_name"]:
                        row += 3
                        if len(data["domain_name"]) > 0: 
                                print( "Updating At Row : "+ str(row)+" data : " + data["domain_name"])
                                sheet.values().update(spreadsheetId=spreadsheet_id, range=f"{sheet_title}!C{row}:C{last_row}",
                                                valueInputOption='RAW', body={"values":[[data["domain_name"]]]}).execute() 
                    
    except Exception as e:
        print(e)
    
    
    # count = 0
    # try:
    #     service = build('sheets', 'v4', credentials=creds)
    #     sheet = service.spreadsheets()
    #     spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
    #     spreadsheet = sheet.get(spreadsheetId=spreadsheet_id).execute()
    #     sheet_properties = spreadsheet.get(
    #         "sheets", [])[sheetNumber].get("properties", "")
    #     sheet_title = sheet_properties.get("title", "")
    #     last_row = sheet_properties.get(
    #         "gridProperties", {}).get("rowCount", 0)
    #     merchant_data = {item.get("merchant_name", ""): item.get("domain_name", "") for item in data}

    #     range_name = f"{sheet_title}!A3:A{last_row}"
        
    #     result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    #     merchant_names = result.get('values', [])
        
    #     # Get the Shopify domain values to compare and update
    #     shopify_col_name_range = f"{sheet_title}!C3:C{last_row}"
    #     shopify_col_name = sheet.values().get(spreadsheetId=spreadsheet_id, range=shopify_col_name_range).execute()
    #     shopify_domain = shopify_col_name.get('values', [])
        
    #     values = []

    #     for row, merchant_name_row in enumerate(merchant_names):
    #         merchant_name = merchant_name_row[0]
    #         domain_name = merchant_data.get(merchant_name, "")
    #         if domain_name and (row >= len(shopify_domain) or not shopify_domain[row]):
    #             values.append([domain_name])
    #         else:
    #             if row < len(shopify_domain):
    #                 values.append([shopify_domain[row][0]])
    #                 count += 1
    #                 counting = str(count) + " injected"
    #                 print(counting)
    #             else:
    #                 values.append([""])  
    #                 count += 1
    #                 counting = str(count) + " empty"
    #                 print(counting)

    #     update_range = f"{sheet_title}!C3:C{last_row}"
    #     update_values = {"values": values}
    #     print(update_values)
    #     sheet.values().update(spreadsheetId=spreadsheet_id, range=update_range,
    #                           valueInputOption='RAW', body=update_values).execute()

    #     return True
    # except HttpError as err:
    #     print(err)
    #     return False
