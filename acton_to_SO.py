import logging
import json
from actonsession import ActonSession

if __name__ == '__main__':
    usr_in = input("Menu \n"
                   "(1) Work with sandbox\n"
                   "(2) Work with live account\n"
                   ">>")

    with open("CREDENTIALS.json") as f:
        credentials = json.loads(f.readline())
        CLIENT_ID = credentials['client-id']
        CLIENT_SECRET = credentials['client-secret']

    if usr_in == 2:
        username = input("Please enter Act-On username")
        password = input("Please enter Act-On password")
    elif usr_in == 1:
        username = 'crmcase@business-sweden.se'
        password = 'welcome'
    else:
        print("No valid selection made, passing on to sandbox")
        username = 'crmcase@business-sweden.se'
        password = 'welcome'

    session = ActonSession()

    # noinspection PyBroadException
    try:
        access_key, refresh_key = session.authenticate(username, password, CLIENT_ID, CLIENT_SECRET)
    except:     # TO BE REMOVED AFTER BUG FIXING
        "Fatal error upon attempt to authenticate. Dropping to shell"
        import code
        code.interact(local=locals())