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

# Validation Of Sheet
def validateSheet():
    global creds
    if os.path.exists(token_path):
        creds = service_account.Credentials.from_service_account_file(
            token_path, scopes=[os.getenv("SCOPES")])
    else:
        print("Data file not found")

# Fetch Data From Sheet
def fetchSheetData(sheetNumber):
    validateSheet()
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        spreadsheet = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = spreadsheet["sheets"][sheetNumber].get("properties", {})
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties["gridProperties"].get("rowCount", 0)
        auto_range = f"{sheet_title}!A3:E{last_row}"

        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=auto_range).execute()
        values = result.get('values', [])
        global merchant_list
        merchant_list = []
        if values:
            for data in values:  
                if len(data[0]) > 1 and len(data[1]) > 1:
                    sheetData = {
                        "merchant_name": data[0],
                        "merchant_url": data[1],
                        "shopify_domain": data[2],
                        "status": data[4],
                        "timeNdate": data[3] if len(data) >= 5 else ""
                    }
                    merchant_list.append(sheetData)
        return merchant_list

    except HttpError as err:
        print("Issue with the Fetch Request")
        return [{"status": False}]

# Remove Duplicates From Sheets
def dataFilter(sheetNumber):
    try:
        validateSheet()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        response = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = response.get("sheets", [])[sheetNumber].get("properties", {})
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties.get(
            "gridProperties", {}).get("rowCount", 0)
        unique_domains = {}
        filtered_data = []
        actualData = fetchSheetData(sheetNumber)
        for index, item in enumerate(actualData,start=3):
            merchant_url = item.get('merchant_url',"").lower()
            merchant_name = item.get('merchant_name',"").lower()
            if merchant_url and merchant_name not in unique_domains :               
                unique_domains[merchant_url] = True
                unique_domains[merchant_name] = True
                filtered_data.append(item)
            else:
                range_str = f"{sheet_title}!A{index}:D{index}"
                sheet.values().clear(
                    spreadsheetId=spreadsheet_id,
                    range=range_str,
                ).execute()
                print(f"Duplicate Record for {item['merchant_name']} at row {str(index)} hence Deleted")
        if filtered_data:
            values_to_write = [[ item['merchant_name'], item['merchant_url'], item['shopify_domain'] , item['timeNdate']] for item in filtered_data]
            update_range = f"{sheet_title}!A3:D{last_row}"
            clear_range = f"{sheet_title}!A3:D{last_row}"
            update_values = {'values': values_to_write}
            sheet.values().clear(
                    spreadsheetId=spreadsheet_id,
                    range=clear_range,
                ).execute()
            sheet.values().update(spreadsheetId=spreadsheet_id, range=update_range,
                                valueInputOption='RAW', body=update_values).execute()
        return filtered_data     
    except Exception as  e:
        print(e)
        print("Issue with Filter Function !!")
        return filtered_data

# Update Domain Name on the Sheet
def writeShopifyDomain(data, sheetNumber):
    try:
        validateSheet()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        response = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = response.get("sheets", [])[sheetNumber].get("properties", {})
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties.get("gridProperties", {}).get("rowCount", 0)

        for row, merchant_name in enumerate(merchant_list, start=3):
            if not merchant_name['shopify_domain']:
                if data and data["merchant_name"] == merchant_name["merchant_name"]:
                    if data["domain_name"]:
                        print(f"Updating At Row: {row}, For Merchant Name: {data['merchant_name']}, has  Domain: {data['domain_name']}")
                        range_str = f"{sheet_title}!C{row}:C{last_row}"
                        values = [[data["domain_name"]]]
                        sheet.values().update(
                            spreadsheetId=spreadsheet_id,
                            range=range_str,
                            valueInputOption='RAW',
                            body={"values": values}
                        ).execute()
                    break
        return True
    except Exception as e:
        print("Error while Fetching Shopify Domain Data")
        print(e)
        return False

# Update Status For API Request    
def writeApiCallData(data,sheetNumber):
    try:
        validateSheet()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        response = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = response.get("sheets", [])[sheetNumber].get("properties", {})
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties.get("gridProperties", {}).get("rowCount", 0)
        if merchant_list:
            for index, data_itms in enumerate(merchant_list,start=3):
                if data_itms["status"] == 'Not Done':
                    if data["merchant_name"] == data_itms["merchant_name"]:
                        if len(data_itms["shopify_domain"]) > 1:
                            print(f"{data['merchant_name']} at row {index} will get the status as {data['status']} ")
                            current_datetime = datetime.datetime.now()
                            update_range = f"{sheet_title}!E{index}:E{last_row}"
                            update_date = f"{sheet_title}!D{index}:D{last_row}"
                            status_update = [[data['status']]]
                            sheet.values().update(
                                    spreadsheetId=spreadsheet_id,
                                    range=update_range,
                                    valueInputOption='RAW',
                                    body={"values": status_update}
                                ).execute()
                            append_values = [[current_datetime.strftime(
                                                     '%Y-%m-%d %H:%M:%S')]]
                            sheet.values().update(
                                    spreadsheetId=spreadsheet_id,
                                    range=update_date,
                                    valueInputOption='RAW',
                                    body={"values": append_values}
                                ).execute()
                                                    
        return True            
    except Exception as e:
        print("Issue in writeApiCallData function")
        return False

# Update Status For API Request for WeeklySheet   
def writeApiCallDataForWeek(data,sheetNumber):
    try:
        validateSheet()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        response = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = response.get("sheets", [])[sheetNumber].get("properties", {})
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties.get("gridProperties", {}).get("rowCount", 0)
        if merchant_list:
            for index, data_itms in enumerate(merchant_list,start=3):
                if data["merchant_name"] == data_itms["merchant_name"]:
                    if len(data_itms["shopify_domain"]) > 1:
                        print(f"{data['merchant_name']} at row {index} will get the status as {data['status']} ")
                        current_datetime = datetime.datetime.now()
                        update_range = f"{sheet_title}!E{index}:E{last_row}"
                        update_date = f"{sheet_title}!D{index}:D{last_row}"
                        status_update = [[data['status']]]
                        sheet.values().update(
                                spreadsheetId=spreadsheet_id,
                                range=update_range,
                                valueInputOption='RAW',
                                body={"values": status_update}
                            ).execute()
                        append_values = [[current_datetime.strftime(
                                                 '%Y-%m-%d %H:%M:%S')]]
                        sheet.values().update(
                                spreadsheetId=spreadsheet_id,
                                range=update_date,
                                valueInputOption='RAW',
                                body={"values": append_values}
                            ).execute()                        
        return True            
    except Exception as e:
        print("Issue in writeApiCallDataForWeek functon")
        return False

# Reattempting Request for Failed Scnearios
def failedScenarioUpdateApiCall(data,sheetNumber):
    try:
        validateSheet()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        response = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = response.get("sheets", [])[sheetNumber].get("properties", {})
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties.get("gridProperties", {}).get("rowCount", 0)
        if merchant_list:
            for index, data_itms in enumerate(merchant_list,start=3):
                if data_itms["status"] == 'Failed' or data_itms["status"] == 'Re-attempted Failed':
                    if data["merchant_name"] == data_itms["merchant_name"]:
                        if len(data_itms["shopify_domain"]) > 1:
                            print(f"{data['merchant_name']} at row {index} will get the status as {data['status']} ")
                            current_datetime = datetime.datetime.now()
                            update_range = f"{sheet_title}!E{index}:E{last_row}"
                            update_date = f"{sheet_title}!D{index}:D{last_row}"
                            status_update = [[data['status']]]
                            sheet.values().update(
                                    spreadsheetId=spreadsheet_id,
                                    range=update_range,
                                    valueInputOption='RAW',
                                    body={"values": status_update}
                                ).execute()
                            append_values = [[current_datetime.strftime(
                                                     '%Y-%m-%d %H:%M:%S')]]
                            sheet.values().update(
                                    spreadsheetId=spreadsheet_id,
                                    range=update_date,
                                    valueInputOption='RAW',
                                    body={"values": append_values}
                                ).execute()
                                                    
        return True            
    except Exception as e:
        print("Issue in writeApiCallData function")
        return False

# Push Data from First Sheet to  Second Sheet 
def pushDataFromFirstToSecond(sheetNumber):
    try:
        validateSheet()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        spreadsheet = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = spreadsheet["sheets"][sheetNumber].get("properties", {})
        sheet_title = sheet_properties.get("title", "")
        responseOfFirstSheet = dataFilter(0)
        responseOfSecondSheet = fetchSheetData(1)
        countOfRow = len(responseOfSecondSheet) + 3
        if responseOfFirstSheet:    
            for index,data in enumerate(responseOfFirstSheet):
                if data.get("status",'') == "Done" or data.get("status",'') == "Re-attempted Success":
                    merchant_name = data.get("merchant_name",'')
                    print(merchant_name)
                    merchant_url = data.get("merchant_url",'')
                    shopify_domain = data.get("shopify_domain",'')
                    status = "Weekly Trigger" 
                    dataNTime = data.get("timeNdate",'')
                    update_values = [[merchant_name, merchant_url, shopify_domain,  dataNTime , status ]] 
                    update_range = f"{sheet_title}!A{countOfRow}:F{countOfRow}"
                    sheet.values().update(
                                spreadsheetId=spreadsheet_id,
                                range=update_range,
                                valueInputOption='RAW',
                                body={"values": update_values}
                            ).execute()
                    countOfRow +=1
        dataFilter(1)            
    except Exception as e:
        print(e)
        print("Issue in Data Pushing Function")


dataFilter(1)