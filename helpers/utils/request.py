import json
import requests

headers = {"Content-Type": "application/json"}
domain = "http://db-api.conext.net.ve"


def get_client_data(body=None):
    try:
        data = json.dumps(body)
        url = f"{domain}/get-client"
        response = requests.post(url, data, headers=headers, verify=False)
        if response.status_code != requests.codes.ok:
            return f"Request failed with status code: {response.status_code}"
        response_json = response.json()
        return response_json
    except requests.RequestException as e:
        return f"An error occurred: {str(e)}"


def add_client_data(body=None):
    try:
        url = f"{domain}/add-client"
        data = json.dumps(body)
        response = requests.post(url, data, headers=headers, verify=False)
        if response.status_code != requests.codes.ok:
            return f"Request failed with status code: {response.status_code}"
        response_json = response.json()
        return response_json
    except requests.RequestException as e:
        # Handle request exceptions
        return f"An error occurred: {str(e)}"


def delete_client_data(body=None):
    try:
        url = f"{domain}/remove-client"
        data = json.dumps(body)
        response = requests.post(url, data, headers=headers, verify=False)
        if response.status_code != requests.codes.ok:
            return f"Request failed with status code: {response.status_code}"
        response_json = response.json()
        return response_json
    except requests.RequestException as e:
        # Handle request exceptions
        return f"An error occurred: {str(e)}"
