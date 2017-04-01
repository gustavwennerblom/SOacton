import logging
import json
from requests.compat import urljoin
from requests.exceptions import HTTPError
from actonsession import ActonSession
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session


if __name__ == '__main__':
    # Create logging instance
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename="SOacton.log", format=FORMAT, level=logging.INFO)

    # Temporary sandbox option exposure
    usr_in = input("Menu \n"
                   "(1) Work with sandbox\n"
                   "(2) Work with live account\n"
                   ">>")

    # Read credentials (only used if working with production environment"
    with open("CREDENTIALS.json") as f:
        credentials = json.loads(f.readline())
        CLIENT_ID = credentials['client-id']
        CLIENT_SECRET = credentials['client-secret']

    HOST = 'https://restapi.actonsoftware.com'

    if usr_in == "2":
        username = input("Please enter Act-On username")
        password = input("Please enter Act-On password")
    elif usr_in == "1":
        username = credentials["sandbox-UID"]
        password = 'welcome'
    else:
        print("No valid selection made, passing on to sandbox")
        username = credentials["sandbox-UID"]
        password = 'welcome'

    # Testing authorization
    path = '/token'
    url = urljoin(HOST, path)
    session = OAuth2Session(client=LegacyApplicationClient(client_id=CLIENT_ID))
    token = session.fetch_token(token_url=url, username=username, password=password,
                                client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    logging.info("Token %s obtained." % token)

    input("Press enter to attempt session refresh")

    # Testing refresh
    # try:
    #     access_key, refresh_key = session.renew_token(CLIENT_ID, CLIENT_SECRET)
    #     logging.info("Successfully refreshed.\n Primary key: {0}, refresh key: {1}".format(access_key, refresh_key))
    # except HTTPError as e:     # TO BE REFINED
    #     print(repr(e))
