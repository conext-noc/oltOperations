import requests


def get_client_data(body=None):
    try:
        url = "http://db-api.conext.net.ve/get-client"
        response = requests.post(url, data=body, verify=False)
        if response.status_code != requests.codes.ok:
            return f"Request failed with status code: {response.status_code}"
        response_json = response.json()
        return response_json
    except requests.RequestException as e:
        # Handle request exceptions
        return f"An error occurred: {str(e)}"


def add_client_data(body=None):
    try:
        url = "http://db-api.conext.net.ve/add-client"
        response = requests.post(url, data=body, verify=False)
        if response.status_code != requests.codes.ok:
            return f"Request failed with status code: {response.status_code}"
        response_json = response.json()
        return response_json
    except requests.RequestException as e:
        # Handle request exceptions
        return f"An error occurred: {str(e)}"


def delete_client_data(body=None):
    try:
        url = "http://db-api.conext.net.ve/remove-client"
        response = requests.post(url, data=body, verify=False)
        if response.status_code != requests.codes.ok:
            return f"Request failed with status code: {response.status_code}"
        response_json = response.json()
        return response_json
    except requests.RequestException as e:
        # Handle request exceptions
        return f"An error occurred: {str(e)}"
