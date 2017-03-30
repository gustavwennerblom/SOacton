import logging
import requests
from requests.compat import urljoin


def wrap(key):
    wrappedkey = '<'+key+'>'
    return wrappedkey


class ActonSession:

    def authenticate(self, username, password, client_id, client_secret):
        path = '/token'
        url = urljoin(self.HOST, path)
        headers = {'Cache-Control': 'no-cache',
                   'Content-Type': 'application/x-www-form-urlencoded'
                   }

        payload = {'grant_type': 'password',
                   'username': username,
                   'password': password,
                   'client_id': client_id,
                   'client_secret': client_secret
                   }

        r = requests.post(url, headers=headers, params=payload)

        # Check that no error has been raised from the request
        if not r.raise_for_status():
            response = r.json()
            self.ACCESS_TOKEN = response['access_token']
            self.REFRESH_TOKEN = response['refresh_token']
            return response['access_token'], response['refresh_token']
        else:
            r.raise_for_status()

    def renew_token(self):
        path = '/token'
        url = urljoin(self.HOST, path)
        headers = {'Cache-Control': 'no-cache',
                   'Content-Type': 'application/x-www-form-urlencoded'
                   }

        payload = {'grant_type': 'refresh_token',
                   'refresh_token': wrap(self.REFRESH_TOKEN),
                   'client_id': wrap(self.CLIENT_ID),
                   'client_secret': wrap(self.CLIENT_SECRET)
                   }

        r = requests.post(url, headers=headers, params=payload)

        if not r.raise_for_status():
            response = r.json()
            self.ACCESS_TOKEN = response['access_token']
            self.REFRESH_TOKEN = response['refresh_token']
        else:
            r.raise_for_status()

    def get_list(self):
        pass

    def __init__(self):
        # Define global variables of host, access token and refresh token
        self.HOST = 'https://restapi.actonsoftware.com'
        self.ACCESS_TOKEN = ''
        self.REFRESH_TOKEN = ''
        self.CLIENT_ID = ''
        self.CLIENT_SECRET = ''

