import requests
import json




def requestTriggered(data):
    url = "https://55e9-103-148-63-122.ngrok-free.app/testApi"
    payload = json.dumps(data)
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text
