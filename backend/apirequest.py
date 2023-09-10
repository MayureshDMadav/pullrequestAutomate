import requests
from dotenv import load_dotenv
import os
import json
import asyncio

load_dotenv()


def testApiCall(data):
    try:
        url= "https://55e9-103-148-63-122.ngrok-free.app/testAPI"
        payload = data
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        res = response.json()      
        if res["status"] == True:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def simplApiPullRequestCall(data):
    try:
        url = os.getenv("SIMPL_URL")
        payload = data
        headers = {
            'Content-Type': 'application/json',
            'SIMPL-SERVICE-ID': os.getenv("SERVICE_ID"),
            'SIMPL-SERVICE-NONCE': os.getenv("SERVICE_NONCE"),
            'SIMPL-SERVICE-SIGNATURE': os.getenv("SERVICE_SIGNATURE")
        }

        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            return True
        else:
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
