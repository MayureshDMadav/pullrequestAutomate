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
    
    
