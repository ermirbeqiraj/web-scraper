import requests
from requests.exceptions import HTTPError

class HttpHelpers:
    def __init__(self):
        self.session = requests.Session()

    def download_page(self, url):
        try:
            response = self.session.get(url)
            response.raise_for_status()
        except HTTPError as httpErr:
            print(f'Http error occurred: {httpErr}')
            return None
        except Exception as err:
            print(f'A generic error occurred: {err}')
            return None
        else:
            return response.content