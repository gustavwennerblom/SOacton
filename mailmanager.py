import json
import logging
from exchangelib import Account, Credentials, DELEGATE, Message, Mailbox


class EWShandler:

    def __init__(self):
        self.authenticated = False
        with open("CREDENTIALS_EWS.json") as j:
            text = j.readline()
            d = json.loads(text)
        self.credentials = Credentials(username=d["UID"], password=d["PWD"])
        logging.info("Successfully authenticated")

    # Authentication presuming a file called
    def authenticate(self, address="crmcase@business-sweden.se"):
        account = Account(primary_smtp_address=address, credentials=self.credentials,
                          autodiscover=True, access_type=DELEGATE)
        logging.info("Authenticated with address {0}".format(address))
        self.authenticated = True
        return account

    # Method to send e-mail without stashing a local copy in "sent"
    def send_mail(self, account, mailbody, recipient="crmcase@business-sweden.se"):

        if not self.authenticated:
            raise EWSLoginError("Error - not authenticated. Call EWShandler.authenticate first")

        m = Message(
            account=account,
            subject="[AUTOGENERATED] From Act-On to SuperOffice",
            body=mailbody,
            to_recipients=[Mailbox(email_address=recipient)]
        )
        logging.info("E-mail message created")
        m.send()
        logging.info("E-mail sent to {0} ".format(recipient))


class EWSLoginError(RuntimeError):
    pass
