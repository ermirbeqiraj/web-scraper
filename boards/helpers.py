import requests
from requests.exceptions import HTTPError

def download_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as httpErr:
        print(f'Http error occurred: {httpErr}')
        return None
    except Exception as err:
        print(f'A generic error occurred: {err}')
        return None
    else:
        return response.content