import os.path
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from datetime import datetime


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
        sheet_properties = spreadsheet["sheets"][sheetNumber].get(
            "properties", {})
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

# FetchDataFromAdhocSheet
def adhocSheetDataReading(sheetNumber):
    validateSheet()
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        spreadsheet = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = spreadsheet["sheets"][sheetNumber].get(
            "properties", {})
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties["gridProperties"].get("rowCount", 0)
        auto_range = f"{sheet_title}!A3:G{last_row}"

        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=auto_range).execute()
        values = result.get('values', [])
        merchant_list = []
        if values:
            for data in values:
                if len(data[0]) > 1 and len(data[1]) > 1:
                    sheetData = {
                        "merchant_name": data[0],
                        "merchant_url": data[1],
                        "shopify_domain": data[2],
                        "start_time": data[3] if len(data[3]) >= 1 else "",
                        "end_time": data[4] if len(data[4]) >= 1 else "",
                        "timeNdate": data[5] if len(data[5]) >= 1 else "",
                        "status": data[6] if len(data[6]) >= 1 else ""
                    }
                    merchant_list.append(sheetData)
        return merchant_list

    except HttpError as err:
        print("Issue with the Fetch Request")
        return [{"status": False}]

# Remove Duplicates From Sheets Not in Action
def dataFilter(sheetNumber):
    try:
        validateSheet()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        response = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = response.get(
            "sheets", [])[sheetNumber].get("properties", {})
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties.get(
            "gridProperties", {}).get("rowCount", 0)
        unique_domains = {}
        filtered_data = []
        actualData = fetchSheetData(sheetNumber)
        for index, item in enumerate(actualData, start=3):
            merchant_url = item.get('merchant_url', "").lower()
            merchant_name = item.get('merchant_name', "").lower()
            if merchant_url and merchant_name not in unique_domains:
                unique_domains[merchant_url] = True
                unique_domains[merchant_name] = True
                filtered_data.append(item)
            else:
                range_str = f"{sheet_title}!A{index}:D{index}"
                sheet.values().clear(
                    spreadsheetId=spreadsheet_id,
                    range=range_str,
                ).execute()
                print(
                    f"Duplicate Record for {item['merchant_name']} at row {str(index)} hence Deleted")
        if filtered_data:
            values_to_write = [[item['merchant_name'], item['merchant_url'],
                                item['shopify_domain'], item['timeNdate']] for item in filtered_data]
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
    except Exception as e:
        print(e)
        print("Issue with Filter Function !!")
        return filtered_data

# Write Data from Front to AdhocRequest Sheet
def writeDataForAdhocFront(dataInput, sheetNumber):
    try:
        validateSheet()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        response = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = response.get(
            "sheets", [])[sheetNumber].get("properties", {})
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties.get(
            "gridProperties", {}).get("rowCount", 0)
        responseOfAdhoc = adhocSheetDataReading(sheetNumber)
        countOfrow = len(responseOfAdhoc) + 3
        for items, data in enumerate(responseOfAdhoc, start=3):
            if dataInput:
                for index, items in enumerate(dataInput):
                    merchant_name = items.get("merchant_name", "")
                    merchant_url = items.get("merchant_url", "")
                    start_time = items.get("start_time", "")
                    end_time = items.get("end_time", "")
                    update_values = [
                        [merchant_name, merchant_url, " ", start_time, end_time, "", "Not Done"]]
                    update_range = f"{sheet_title}!A{countOfrow}:G{countOfrow}"
                    sheet.values().update(
                        spreadsheetId=spreadsheet_id,
                        range=update_range,
                        valueInputOption='RAW',
                        body={"values": update_values}
                    ).execute()
                    countOfrow += 1
                return True
            else:
                return False

    except Exception as e:
        print(e)

# Update Domain Name on the Sheet
def writeShopifyDomain(data, sheetNumber):
    try:
        validateSheet()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        response = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = response.get(
            "sheets", [])[sheetNumber].get("properties", {})
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties.get(
            "gridProperties", {}).get("rowCount", 0)

        for row, merchant_name in enumerate(merchant_list, start=3):
            if not merchant_name['shopify_domain']:
                if data and data["merchant_name"] == merchant_name["merchant_name"]:
                    if data["domain_name"]:
                        print(
                            f"Updating At Row: {row}, For Merchant Name: {data['merchant_name']}, has  Domain: {data['domain_name']}")
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
        return False

# Update Status For API Request
def writeApiCallData(data, sheetNumber):
    try:
        validateSheet()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        response = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = response.get(
            "sheets", [])[sheetNumber].get("properties", {})
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties.get(
            "gridProperties", {}).get("rowCount", 0)
        if merchant_list:
            for index, data_itms in enumerate(merchant_list, start=3):
                if data_itms["status"] == 'Not Done':
                    if data["merchant_name"] == data_itms["merchant_name"]:
                        if len(data_itms["shopify_domain"]) > 1:
                            print(
                                f"{data['merchant_name']} at row {index} will get the status as {data['status']} ")
                            current_datetime = datetime.now()
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
        print(e)
        return False

# Update Status For API Request for WeeklySheet
def writeApiCallDataForWeek(data, sheetNumber):
    try:
        validateSheet()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        response = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = response.get(
            "sheets", [])[sheetNumber].get("properties", {})
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties.get(
            "gridProperties", {}).get("rowCount", 0)
        if merchant_list:
            for index, data_itms in enumerate(merchant_list, start=3):
                if data["merchant_name"] == data_itms["merchant_name"]:
                    if len(data_itms["shopify_domain"]) > 1:
                        print(
                            f"{data['merchant_name']} at row {index} will get the status as {data['status']} ")
                        current_datetime = datetime.now()
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
        print("Issue in writeApiCallDataForWeek function")
        return False

# Update Data for Adhoc Request Sheet
def writeApiCallDataForAdhoc(data, sheetNumber):
    try:
        validateSheet()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        response = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = response.get(
            "sheets", [])[sheetNumber].get("properties", {})
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties.get(
            "gridProperties", {}).get("rowCount", 0)
        if merchant_list:
            for index, data_itms in enumerate(merchant_list, start=3):
                if data["merchant_name"] == data_itms["merchant_name"]:
                    if len(data_itms["shopify_domain"]) > 1:
                        print(
                            f"{data['merchant_name']} at row {index} will get the status as {data['status']} ")
                        current_datetime = datetime.now()
                        update_range = f"{sheet_title}!G{index}:G{last_row}"
                        update_date = f"{sheet_title}!F{index}:F{last_row}"
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
        print("Issue in writeApiCallDataForWeek function")
        return False

# Reattempting Request for Failed Scenario
def failedScenarioUpdateApiCall(data, sheetNumber):
    try:
        validateSheet()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        response = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = response.get(
            "sheets", [])[sheetNumber].get("properties", {})
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties.get(
            "gridProperties", {}).get("rowCount", 0)
        if merchant_list:
            for index, data_itms in enumerate(merchant_list, start=3):
                if data_itms["status"] == 'Failed' or data_itms["status"] == 'Re-attempted Failed':
                    if data["merchant_name"] == data_itms["merchant_name"]:
                        if len(data_itms["shopify_domain"]) > 1:
                            print(
                                f"{data['merchant_name']} at row {index} will get the status as {data['status']} ")
                            current_datetime = datetime.now()
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
        sheet_properties = spreadsheet["sheets"][sheetNumber].get(
            "properties", {})
        sheet_title = sheet_properties.get("title", "")
        responseOfFirstSheet = fetchSheetData(0)
        responseOfSecondSheet = fetchSheetData(sheetNumber)
        countOfRow = len(responseOfSecondSheet) + 3
        if responseOfFirstSheet:
            for index, data in enumerate(responseOfFirstSheet):
                date_object = datetime.strptime(
                    data.get("timeNdate", ""), "%Y-%m-%d %H:%M:%S")
                current_date = datetime.now()
                current_date_n_time = datetime.strptime(
                    str(current_date), "%Y-%m-%d %H:%M:%S.%f")
                extracted_date_sheet = date_object.strftime("%Y-%m-%d")
                current_date_for_sheet = current_date_n_time.strftime(
                    "%Y-%m-%d")
                if extracted_date_sheet == current_date_for_sheet:
                    if data.get("status", '') == "Done" or data.get("status", '') == "Re-attempted Success":
                        merchant_name = data.get("merchant_name", '')
                        print(merchant_name)
                        merchant_name = data.get("merchant_name", '')
                        merchant_url = data.get("merchant_url", '')
                        shopify_domain = data.get("shopify_domain", '')
                        status = "Weekly Trigger"
                        dataNTime = data.get("timeNdate", '')
                        update_values = [
                            [merchant_name, merchant_url, shopify_domain,  dataNTime, status]]
                        update_range = f"{sheet_title}!A{countOfRow}:F{countOfRow}"
                        sheet.values().update(
                            spreadsheetId=spreadsheet_id,
                            range=update_range,
                            valueInputOption='RAW',
                            body={"values": update_values}
                        ).execute()
                        countOfRow += 1
            fetchSheetData(1)
    except Exception as e:
        print("Issue in Data Pushing Function")
        print(e)

# Push Data from SalesForce Sheet to First Sheet
def pushDataFromSalesForceToFirst(sheetNumber):
    try:
        validateSheet()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        spreadsheet = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = spreadsheet["sheets"][sheetNumber].get(
            "properties", {})
        sheet_title = sheet_properties.get("title", "")
        responseOfFourthSheet = fetchSheetData(sheetNumber)
        responseOfFirstSheet = fetchSheetData(0)
        countOfRow = len(responseOfFirstSheet) + 3
        if responseOfFourthSheet:
            for index, data in enumerate(responseOfFourthSheet):
                if data:
                    merchant_name = data.get("merchant_name", '')
                    merchant_url = data.get("merchant_url", '')
                    update_values = [[merchant_name, merchant_url]]
                    update_range = f"{sheet_title}!A{countOfRow}:F{countOfRow}"
                    sheet.values().update(
                        spreadsheetId=spreadsheet_id,
                        range=update_range,
                        valueInputOption='RAW',
                        body={"values": update_values}
                    ).execute()
                    countOfRow += 1
        fetchSheetData(1)
    except Exception as e:
        print(e)
        print("Issue in Data Pushing Function")







