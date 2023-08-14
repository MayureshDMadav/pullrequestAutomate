from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import os.path
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import time
import datetime
from selenium.webdriver.chrome.service import Service

load_dotenv()

current_dir = os.path.dirname(__file__)
token_path = os.path.join(current_dir, 'keys.json')

creds = None


# validate the sheet
def validateSheet():
    global creds
    if os.path.exists(token_path):
        creds = service_account.Credentials.from_service_account_file(
            token_path, scopes=[os.getenv("SCOPES")])
    else:
        print("Data file not found")


# Reading Data From the Sheet

# DATA from sheet 1
def everyDaySheetReading():
    validateSheet()
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet = sheet.get(spreadsheetId=os.getenv(
            "SAMPLE_SPREADSHEET_ID")).execute()
        sheet_properties = spreadsheet.get(
            "sheets", [])[0].get("properties", {})
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

        # Fetching the List of Merchants that are available
        merchant_list = []
        for row in values:
            jsonData = {"merchant_name": row[0],
                        "merchant_url": row[1], "status": row[2]}
            merchant_list.append(jsonData)

        # Removing the Headers
        if len(merchant_list) > 0:
            merchant_list.pop(0)
        else:
            print("Merchant List is empty")

        # Getting List of Merchant and Values
        return merchant_list

    except HttpError as err:
        print(err)
        return "No Sheet to connect"


# DATA from sheet 2

def weeklyDataSheetReading():
    validateSheet()
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet = sheet.get(spreadsheetId=os.getenv(
            "SAMPLE_SPREADSHEET_ID")).execute()
        sheet_properties = spreadsheet.get(
            "sheets", [])[1].get("properties", {})
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

        # Fetching the List of Merchants that are available
        merchant_list = []
        for row in values:
            jsonData = {"merchant_name": row[0],
                        "merchant_url": row[1], "status": row[2]}
            merchant_list.append(jsonData)

        # Removing the Headers
        if len(merchant_list) > 0:
            merchant_list.pop(0)
        else:
            print("Merchant List is empty")

        # Getting List of Merchant and Values
        return merchant_list

    except HttpError as err:
        print(err)
        return "No Sheet to connect"


# Data Writing
# Every Next Day Schedule for status not done
# def everyDaySheetNetxDayWriting(data):
    validateSheet()
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        spreadsheet = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = spreadsheet.get(
            "sheets", [])[0].get("properties", {})
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties.get(
            "gridProperties", {}).get("rowCount", 0)
        # Fetch data from the sheet
        merchant_data = {}
        if data:
            for item in data:
                merchant_name = next(iter(item))
                status = item[merchant_name]
                merchant_data[merchant_name] = status
        # Fetch merchant names from the first column (A) of the sheet
        range_name = f"{sheet_title}!A2:A{last_row}"
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        merchant_names = result.get('values', [])
        values = []
        for row, merchant_name_row in enumerate(merchant_names):
            merchant_name = merchant_name_row[0]
            status = 'Done' if merchant_data.get(
                merchant_name, False) else 'Not Done'
            values.append([status])
        # Update the values in the Status column (column C)
        update_range = f"{sheet_title}!C2:C{last_row}"
        update_values = {'values': values}
        sheet.values().update(spreadsheetId=spreadsheet_id, range=update_range,
                              valueInputOption='RAW', body=update_values).execute()
        return True
    except HttpError as err:
        print(err)
        return False

# Data write to Sheet 1


def everyDaySheetNetxDayWriting(data):
    validateSheet()
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet_id = os.getenv("SAMPLE_SPREADSHEET_ID")
        spreadsheet = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheet_properties = spreadsheet.get(
            "sheets", [])[0].get("properties", {})
        sheet_title = sheet_properties.get("title", "")
        last_row = sheet_properties.get(
            "gridProperties", {}).get("rowCount", 0)

        merchant_data = {}
        if data:
            for item in data:
                merchant_name = next(iter(item))
                status = item[merchant_name]
                merchant_data[merchant_name] = status

        range_name = f"{sheet_title}!A2:A{last_row}"
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        merchant_names = result.get('values', [])
        values = []

        for row, merchant_name_row in enumerate(merchant_names):
            merchant_name = merchant_name_row[0]
            status = 'Done' if merchant_data.get(
                merchant_name, False) else 'Not Done'
            values.append([status])

        update_range = f"{sheet_title}!C2:C{last_row}"
        update_values = {'values': values}
        sheet.values().update(spreadsheetId=spreadsheet_id, range=update_range,
                              valueInputOption='RAW', body=update_values).execute()

        current_datetime = datetime.datetime.now()
        append_values = [[current_datetime.strftime(
            '%Y-%m-%d %H:%M:%S')]] * len(merchant_names)
        append_range = f"{sheet_title}!D2:D{last_row}"
        append_body = {'values': append_values}
        sheet.values().update(spreadsheetId=spreadsheet_id, range=append_range,
                              valueInputOption='RAW', body=append_body).execute()

        return True
    except HttpError as err:
        print(err)
        return False
