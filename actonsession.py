import html
import logging
import requests
from requests.compat import urljoin
import time
import DBmanager


class ActonSession:

    @staticmethod
    def wrap(key):
        wrappedkey = html.escape("<") + key + html.escape(">")
        return wrappedkey

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
            self.db.insert_tokens(self.ACCESS_TOKEN, self.REFRESH_TOKEN)
            return response['access_token'], response['refresh_token']
        else:
            r.raise_for_status()

    def renew_token(self, client_id, client_secret):
        path = '/token'
        url = urljoin(self.HOST, path)
        headers = {'Cache-Control': 'no-cache',
                   'Content-Type': 'application/x-www-form-urlencoded'
                   }

        payload = {'grant_type': 'refresh_token',
                   'refresh_token': self.REFRESH_TOKEN,
                   'client_id': client_id,
                   'client_secret': client_secret
                   }

        r = requests.post(url, headers=headers, params=payload)
        # print("Request: {}".format(r.text))

        if not r.raise_for_status():
            response = r.json()
            # print("Response: {}".format(response))
            self.ACCESS_TOKEN = response['access_token']
            self.REFRESH_TOKEN = response['refresh_token']
            return self.ACCESS_TOKEN, self.REFRESH_TOKEN
        else:
            r.raise_for_status()

    # Gets list of lists
    # Returns a dict with keys "result", "count" (length), "totalCount", and "offset"
    # response["result"] is a list
    # resonse["result"][0] is a dict with a key "name" holding the name of the list
    def get_lists(self, listing_type="CONTACT_LIST"):

        path = '/api/1/list'
        url = urljoin(self.HOST, path)
        token = self.db.get_token()
        auth = 'Bearer ' + token
        headers = {'Cache-Control': 'no-cache', 'Authorization': auth}

        payload = {'listingtype': listing_type}

        response = requests.get(url, headers=headers, params=payload)
        return response.json()

    def __init__(self):
        # Define global variables of host, access token and refresh token
        self.HOST = 'https://restapi.actonsoftware.com'
        self.ACCESS_TOKEN = ''
        self.REFRESH_TOKEN = ''
        self.CLIENT_ID = ''
        self.CLIENT_SECRET = ''
        self.db = DBmanager.DBmanager()
        self.LEASE_TIME = 3600  # key lease time in seconds