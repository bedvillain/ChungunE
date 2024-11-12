import requests

def get_school_data_from_api():
    url = ""
    response = requests.get(url)
    return response.json()