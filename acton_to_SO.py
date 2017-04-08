import logging
import json
from requests.exceptions import HTTPError
from actonsession import ActonSession


def validate_intention(message):
    usr_in = input(message + " Continue? (Y/N)")
    if usr_in.upper() == "Y":
        return True
    else:
        return False


def test_authenticate(session):

    if validate_intention("This function will return accesskey and refresh key that you might want to save."):
        try:
            access_key, refresh_key = session.authenticate(username, password, CLIENT_ID, CLIENT_SECRET)
            logging.info("Successfully authenticated.\n Primary key: {0}, refresh key: {1}".format(access_key, refresh_key))
            return access_key, refresh_key
        except HTTPError as e:
            print("Fatal error upon attempt to authenticate")
            print(repr(e))
    else:
        print("Aborting")
        logging.warning("User aborted authentication method")
        return None


def test_refresh(session):
    if validate_intention("This function will return accesskey and refresh key that you might want to save."):
        try:
            access_key, refresh_key = session.renew_token(CLIENT_ID, CLIENT_SECRET)
            logging.info("Successfully refreshed.\n Primary key: {0}, refresh key: {1}".format(access_key, refresh_key))
        except HTTPError as e:  # TO BE REFINED
            print(repr(e))
    else:
        logging.warning("User aborted authentication method")
        return None


def test_getlists(session):
    if validate_intention("This returns a dict of contact lists in account."):
        list_dict = session.get_list()
        return list_dict
    else:
        return None

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

    print("Methods available:"
          "\n\t test_authenticate (takes 'session' in, returns keys)"
          "\n\t test_refresh (takes 'session' in returns keys)"
          "\n\t test_getlists (takes 'session' in, returns dict")

    # Drop to shell to interact with test methods
    import code
    code.interact(local=locals())

