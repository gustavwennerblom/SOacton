import logging
import json
import pprint
from requests.exceptions import HTTPError
from actonsession import ActonSession
from mailmanager import EWShandler

# Create logging instance
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename="SOacton.log", format=FORMAT, level=logging.DEBUG)


def validate_intention(message):
    usr_in = input(message + " Continue? (Y/N)")
    if usr_in.upper() == "Y":
        return True
    else:
        return False


def test_authenticate(session):
    logging.info("Attempting to authenticate")
    if validate_intention("This function will return accesskey and refresh key that you might want to save."):
        try:
            access_key, refresh_key = session.authenticate(username, password, CLIENT_ID, CLIENT_SECRET)
            logging.info("Successfully authenticated. Primary key: {0}, refresh key: {1}".format(access_key, refresh_key))
            return access_key, refresh_key
        except HTTPError as e:
            print("Fatal error upon attempt to authenticate")
            print(repr(e))
    else:
        print("Aborting")
        logging.warning("User aborted authentication method")
        return None


def test_refresh(session):
    logging.info("Attempting refresh of access key")
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
        list_dict = session.get_lists()
        logging.info("Successful - lists returned (hope you caught it...)")
        return list_dict
    else:
        return None


def test_glbn(session, list_name):
    if validate_intention("This returns a contact list represented as a dict"):
        try:
            list_dict = session.get_list_by_name(list_name)
            return list_dict
        except ValueError as e:
            logging.error(repr(e))
            print('!!!! ' + repr(e))
    else:
        return None


def test_get_core_data(session, list_name):
    if not validate_intention("This prints core contact list data to stdout"):
        return None

    contacts = test_glbn(session, list_name)

    # Build dict with index of targetted headers
    target_headers = ["E-mail Address",
                      "First Name",
                      "Last Name",
                      "Company",
                      "Act-On score"]
    indices = {}
    for header in contacts["headers"]:
        if header in target_headers:
            indices[header] = contacts["headers"].index(header)
            logging.info("Index of {0} set to {1}".format(header, indices[header]))

    for person in contacts["data"]:
        print("First Name: {0}, Last Name: {1}, Email:{2}, Company: {3}, Act-On score: {4}"
              .format(person[indices["First Name"]],
                      person[indices["Last Name"]],
                      person[indices["E-mail Address"]],
                      person[indices["Company"]],
                      person[indices["Act-On score"]]))


# Returns a list of lists with certain defined fields
def get_core_data(session, list_name):
    if not validate_intention("This returns a dict with the core data in a given list"):
        return None

    contacts = test_glbn(session, list_name)

    # Build dict with index of targetted headers
    target_headers = ["E-mail Address",
                      "First Name",
                      "Last Name",
                      "Company",
                      "Act-On score"]
    indices = {}
    for header in contacts["headers"]:
        if header in target_headers:
            indices[header] = contacts["headers"].index(header)
            logging.info("Index of {0} set to {1}".format(header, indices[header]))

    # Build up return dict core_data
    core_data = []
    for person in contacts["data"]:
        core_data.append([person[indices["E-mail Address"]],
                         person[indices["First Name"]],
                         person[indices["Last Name"]],
                         person[indices["Company"]],
                         person[indices["Act-On score"]]])

    return core_data


# Prints names of lists in account to stdout
def test_print_lists(session):
    contactlists = test_getlists(session)
    for listname in contactlists["result"]:
        print(listname["name"])


# Sends email via EWS, given a specific body text
def send_mail(body):

    mailman = EWShandler()
    EWS_session = mailman.authenticate()

    mailman.send_mail(EWS_session, body)


# Prepares email on prescribed format and forwards it to send_mail()
def mail_core_data(session):
    data = get_core_data(session, "All scored contacts")
    labels = ["E-mail: ", "Firstname: ", "Lastname: ", "Company: ", "Act-On Score: "]
    body = "DATA BEGIN\n"
    delim = "--\n"
    for record in data:
        body += delim
        for i in range(5):
            fragment = labels[i] + record[i] + "\n"
            body += fragment
    body += "--\nDATA END. GOODBYE."

    # Pass on the constructed mail body to the emailer
    send_mail(body)


if __name__ == '__main__':
    # Temporary sandbox option exposure
    usr_in = input("Menu \n"
                   "(1) Work with sandbox\n"
                   "(2) Work with live account\n"
                   ">>")

    # Read credentials
    with open("CREDENTIALS.json") as f:
        credentials = json.loads(f.readline())
        CLIENT_ID = credentials['client-id']
        CLIENT_SECRET = credentials['client-secret']

    HOST = 'https://restapi.actonsoftware.com'

    # Take username and password from stdin if opting to use live environment
    if usr_in == "2":
        username = input("Please enter Act-On username")
        password = input("Please enter Act-On password")
    # Fast route if using sandbox
    elif usr_in == "1":
        username = credentials["sandbox-UID"]
        password = 'welcome'
    else:
        print("No valid selection made, passing on to sandbox")
        username = credentials["sandbox-UID"]
        password = 'welcome'

    # Create session manager instance aware of CLIENT_ID and CLIENT_SECRET
    session = ActonSession(CLIENT_ID, CLIENT_SECRET)

    print("Methods available:"
          "\n\t test_authenticate (takes 'session' in, returns keys)"
          "\n\t test_refresh (takes 'session' in returns keys)"
          "\n\t test_getlists (takes 'session' in, returns dict"
          "\n\t test_glbn (takes session and list name in, returns dict)"
          "\n\t test_get_core_data (takes session and list name, prints to stdout)"
          "\n\t get_core_data (takes sesison and list name, returns list of lists)"
          "\n\t test_print_lists (takes session in, prints list names to stdout)"
          "\n\t send_mail sends a mail with body as specified in argument"
          "\n\t (Use 'pp.pprint(dict)' to pretty print dicts)")

    pp = pprint.PrettyPrinter(indent=2)

    # Drop to shell to interact with test methods
    import code
    code.interact(local=locals())
