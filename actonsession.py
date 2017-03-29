import requests
from requests.compat import urljoin

# Define global variables of host, access token and refresh token
HOST = 'https://restapi.actonsoftware.com'
ACCESS_TOKEN = ""
REFRESH_TOKEN = ""

def authorize(username, password):
    path = '/token'
    url = urljoin(HOST, path)
    headers = {'Cache-Control': 'no-cache',
               'Content-Type': 'application/x-www-form-urlencoded'
               }

    payload = {'grant_type': 'password',
               'username': username
               'password': password,
               'client_id': 'UNKNOWN',
               'client_secret': 'UNKNOWN'
               }

    r = requests.post(url, headers=headers, params=payload)
    import code
    code.interact(local=locals())

    # Check that no error has been raised from the request
    if not r.raise_for_status():
        response = r.json()
        ACCESS_TOKEN = response['access_token']
        REFRESH_TOKEN = response['refresh_token']

def get_list():



if __name__ == '__main__':
    username = input("Please enter Act-On username")
    password = input("Please enter Act-On password")
    authorize(username, password)
