from datetime import datetime, timedelta
import json


def get_current_date():
    current_date = datetime.now()
    year = current_date.year
    month = str(current_date.month).zfill(2)
    date = str(current_date.day).zfill(2)
    return f"{year}-{month}-{date}"


def get_last_fourth_date():
    current_date = datetime.now()
    fourth_day = current_date + timedelta(days=-4)
    year = current_date.year
    month = str(current_date.month).zfill(2)
    date = str(fourth_day.day).zfill(2)
    return f"{year}-{month}-{date}"    

def get_previous_date_time():
    now = datetime.now()  # Get current local date and time
    previous_day = now - timedelta(days=1)
    year = previous_day.year
    month = str(previous_day.month).zfill(2)
    day = str(previous_day.day).zfill(2)
    hours = str(previous_day.hour).zfill(2)
    minutes = str(previous_day.minute).zfill(2)
    seconds = str(previous_day.second).zfill(2)
    return f"{year}-{month}-{day}T{hours}:{minutes}:{seconds}Z"


def get_time_format_for_adhoc():
    dateTime = datetime.now()
    hours = str(dateTime.hour).zfill(2)
    minutes = str(dateTime.minute).zfill(2)
    seconds = str(dateTime.second).zfill(2)
    return f"T{hours}:{minutes}:{seconds}Z"


def createRequestForPost(data):
    if data:
        jsonRequest = {}
        jsonRequest["store_domain"] = data
        jsonRequest["pull_type"] = "customer_info"
        jsonRequest["reason"] = "address ingestion"
        jsonRequest["run_by"] = "mayuresh.madav@getsimpl.com"
        jsonRequest["start_date"] = "2021-12-31T18:29:29Z"
        jsonRequest["end_date"] = get_previous_date_time()

    response = json.dumps(jsonRequest)
    return response


def createRequestForPostAdhoc(startTime, endTime, data):
    if data:
        jsonRequest = {}
        jsonRequest["store_domain"] = data
        jsonRequest["pull_type"] = "customer_info"
        jsonRequest["reason"] = "address ingestion"
        jsonRequest["run_by"] = "mayuresh.madav@getsimpl.com"
        jsonRequest["start_date"] = str(
            startTime + get_time_format_for_adhoc())
        jsonRequest["end_date"] = str(endTime + get_time_format_for_adhoc())

    response = json.dumps(jsonRequest)
    return response
