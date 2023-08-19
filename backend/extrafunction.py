import datetime
import json


def get_previous_date_time():
    now = datetime.datetime.now()  # Get current local date and time
    previous_day = now - datetime.timedelta(days=1)
    year = previous_day.year
    month = str(previous_day.month).zfill(2)
    day = str(previous_day.day).zfill(2)
    hours = str(previous_day.hour).zfill(2)
    minutes = str(previous_day.minute).zfill(2)
    seconds = str(previous_day.second).zfill(2)
    return f"{year}-{month}-{day}T{hours}:{minutes}:{seconds}Z"


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
