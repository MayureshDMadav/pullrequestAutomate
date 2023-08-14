import requests
from dotenv import load_dotenv
import os
import json
import asyncio

load_dotenv()


def requestTriggered(data):
    url = "https://55e9-103-148-63-122.ngrok-free.app/testApi"
    payload = json.dumps(data)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


task_count = 0


async def simplApiPullRequestCall(data):
    try:
        global task_count
        url = os.getenv("SIMPL_URL")
        payload = json.dumps(data)
        task_count += 1
        print(task_count)
        headers = {
            'Content-Type': 'application/json',
            'SIMPL-SERVICE-ID': os.getenv("SERVICE_ID"),
            'SIMPL-SERVICE-NONCE': os.getenv("SERVICE_NONCE"),
            'SIMPL-SERVICE-SIGNATURE': os.getenv("SERVICE_SIGNATURE")
        }

        response = await asyncio.to_thread(requests.post, url, headers=headers, data=payload)

        if response.status_code == 200:
            return True
        else:
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
