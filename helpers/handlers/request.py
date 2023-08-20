import os
import json
from dotenv import load_dotenv
import requests
from helpers.constants import definitions

domain = definitions.domain
headers = definitions.headers

load_dotenv()


def db_request(endpoint: str, data: dict):
    data["API_KEY"] = os.environ["API_KEY"]
    payload = json.dumps(data)
    url = f"{domain}{endpoint}"
    try:
        response = requests.post(url, data=payload, headers=headers, verify=False)
        if response.status_code != requests.codes.ok:
            return {
                "error": True,
                "data": None,
                "message": f"Request failed with status code: {response.status_code}",
            }
        response_json = response.json()
        return response_json
    except requests.RequestException as e:
        return {"error": True, "message": f"An error occurred: {str(e)}", "data": None}


db_request(
    "update-client",
    {
        "lookup_type": "C",
        "lookup_value": "0000777773",
        "API_KEY": "pykboz-metcew-fihVe2K2.p##/5We$tt!&",
        "change_field": "OX",
        "new_values": "deactivated",
    },
)
