import os
import json
from dotenv import load_dotenv
import requests

load_dotenv()

headers = {"Content-Type": "application/json"}
domain = "http://db-api.conext.net.ve"


def get_client_data(payload, lookup):
    url = f"{domain}/get-client"
    data = json.dumps(
        {
            "API_KEY": os.environ["API_KEY"],
            "lookup_type": lookup,
            "lookup_value": payload,
        }
    )
    return db_request(url, data)


def add_client_data(payload):
    url = f"{domain}/add-client"
    data = json.dumps(
        {
            "API_KEY": os.environ["API_KEY"],
            "client": {
                "frame": str(payload["frame"]),
                "slot": str(payload["slot"]),
                "port": str(payload["port"]),
                "onu_id": str(payload["onu_id"]),
                "name": payload["name"],
                "status": "online",
                "pwr": payload["pwr"],
                "state": "active",
                "last_down_cause": "dying-gasp",
                "last_down_time": "-",
                "last_down_date": "-",
                "sn": payload["sn"],
                "device": payload["device"],
                "vlan": payload["wan"][0]["provider"],
                "fsp": f"{payload['frame']}/{payload['slot']}/{payload['port']}",
            },
        }
    )
    return db_request(url, data)


def delete_client_data(payload, lookup):
    url = f"{domain}/remove-client"
    data = json.dumps(
        {
            "API_KEY": os.environ["API_KEY"],
            "lookup_type": lookup,
            "lookup_value": payload,
        }
    )
    return db_request(url, data)


def modify_client_data(payload, lookup, change, new_value):
    url = f"{domain}/update-client"
    data = json.dumps(
        {
            "API_KEY": os.environ["API_KEY"],
            "lookup_value": payload,
            "lookup_type": lookup,
            "change_field": change,
            "new_values": new_value,
        }
    )
    return db_request(url, data)


def db_request(url, data):
    try:
        response = requests.post(url, data, headers=headers, verify=False)
        if response.status_code != requests.codes.ok:
            return f"Request failed with status code: {response.status_code}"
        response_json = response.json()
        return response_json
    except requests.RequestException as e:
        return f"An error occurred: {str(e)}"
