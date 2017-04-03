import logging
import json
from requests.exceptions import HTTPError
from actonsession import ActonSession


if __name__ == '__main__':
    # Create logging instance
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename="SOacton.log", format=FORMAT, level=logging.DEBUG)

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

    # Create session manager instance
    session = ActonSession()

    # Testing authorization
    try:
        access_key, refresh_key = session.authenticate(username, password, CLIENT_ID, CLIENT_SECRET)
        logging.info("Successfully authenticated.\n Primary key: {0}, refresh key: {1}".format(access_key, refresh_key))
    except HTTPError as e:
        print("Fatal error upon attempt to authenticate. Dropping to shell")
        print(repr(e))

    input("Press enter to attempt session refresh")

    # Testing refresh
    try:
        access_key, refresh_key = session.renew_token(CLIENT_ID, CLIENT_SECRET)
        logging.info("Successfully refreshed.\n Primary key: {0}, refresh key: {1}".format(access_key, refresh_key))
    except HTTPError as e:     # TO BE REFINED
        print(repr(e))

    input("Press enter to attempt getting a contact list")

    # Get list of contact lists
    list_dict = session.get_list(access_key)
    import code
    code.interact(local=locals())

