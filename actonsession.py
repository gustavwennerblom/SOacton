import html
import logging
import requests
from requests.compat import urljoin
import datetime
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
            access_token = response['access_token']
            refresh_token = response['refresh_token']
            self.db.insert_tokens(access_token, refresh_token)
            return access_token, refresh_token
        else:
            r.raise_for_status()

    def renew_token(self, client_id, client_secret):
        path = '/token'
        url = urljoin(self.HOST, path)
        headers = {'Cache-Control': 'no-cache',
                   'Content-Type': 'application/x-www-form-urlencoded'
                   }

        payload = {'grant_type': 'refresh_token',
                   'refresh_token': self.db.get_refresh_token(),
                   'client_id': client_id,
                   'client_secret': client_secret
                   }

        r = requests.post(url, headers=headers, params=payload)

        if not r.raise_for_status():
            response = r.json()
            # print("Response: {}".format(response))
            access_token = response['access_token']
            refresh_token = response['refresh_token']
            self.db.insert_tokens(access_token, refresh_token)
            return access_token, refresh_token
        else:
            r.raise_for_status()

    # Gets list of lists
    # Returns a dict with keys "result", "count" (length), "totalCount", and "offset"
    # response["result"] is a list
    # resonse["result"][0] is a dict with a key "name" holding the name of the list
    def get_lists(self, listing_type="CONTACT_LIST"):
        # Check if token has expired and renew it if required
        logging.info("Triggering check for token validity...")
        if not self.token_valid():
            self.renew_token(self.CLIENT_ID, self.CLIENT_SECRET)

        path = '/api/1/list'
        url = urljoin(self.HOST, path)
        token = self.db.get_token()
        auth = 'Bearer ' + token
        headers = {'Cache-Control': 'no-cache', 'Authorization': auth}

        payload = {'listingtype': listing_type}

        response = requests.get(url, headers=headers, params=payload)
        return response.json()

    def token_valid(self):
        logging.info("Checking token validity....")
        current_key_timestamp = self.db.get_key_timestamp()  # returns a datetime object
        lifetime = datetime.datetime.now() - current_key_timestamp
        if lifetime.seconds < self.LEASE_TIME:
            logging.info("Current access key in use for {0} seconds. Max lease time is {1}. OK to proceed with it"
                         .format(lifetime.seconds, self.LEASE_TIME))
            return True
        else:
            logging.info("Current access key has expired (in use since {0} seconds, max lease time is {1} seconds)."
                         "Suggesting to renew".format(lifetime.seconds, self.LEASE_TIME))
            return False

    def __init__(self, client_id, client_secret):
        # Define global variables of host, access token and refresh token
        self.HOST = 'https://restapi.actonsoftware.com'
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.db = DBmanager.DBmanager()
        self.LEASE_TIME = 3600  # key lease time in seconds
