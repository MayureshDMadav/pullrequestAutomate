import datetime
import json


def get_current_date_time():
    now = datetime.datetime.now()  # Get current local date and time
    year = now.year
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)
    hours = str(now.hour).zfill(2)
    minutes = str(now.minute).zfill(2)
    seconds = str(now.second).zfill(2)
    return f"{year}-{month}-{day}T{hours}:{minutes}:{seconds}Z"


def createRequestForPost(data):
    if data:
        jsonRequest = {}
        jsonRequest["store_domain"] = data["merchant_url"]
        jsonRequest["pull_type"] = "customer_info"
        jsonRequest["reason"] = "address ingestion"
        jsonRequest["run_by"] = "mayuresh.madav@getsimpl.com"
        jsonRequest["start_date"] = "2021-12-31T18:29:29Z"
        jsonRequest["end_date"] = get_current_date_time()

    response = json.dumps(jsonRequest)
    return response
