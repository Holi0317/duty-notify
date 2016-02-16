#!/usr/bin/env python3

import argparse

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools
from apiclient.discovery import build
from httplib2 import Http

from utils.logger import logger

MORNING_URL = 'http://mail.stmarks.edu.hk/~smssmf/morning.htm'
ASSEMBLY_URL = 'http://mail.stmarks.edu.hk/~smssmf/assembly.htm'

OAUTH2_SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


def main():
    logger.info('Started.')

    http = make_google()


def make_google():
    """
    Request for credentials from Google OAuth2.
    After request, save them into credentials file.

    return -- httplib2 http object with Google OAuth2 authorized.
    """
    storage = Storage('credentials')
    creds = storage.get()

    if not creds or creds.invalid:

        parser = argparse.ArgumentParser(parents=[tools.argparser])
        flags = parser.parse_args()

        flow = flow_from_clientsecrets('client_id.json',
                                       scope=OAUTH2_SCOPES)
        flow.params['access_type'] = 'offline'
        creds = tools.run_flow(flow, storage, flags)
        storage.put(creds)

    return creds.authorize(Http())


if __name__ == "__main__":
    main()
