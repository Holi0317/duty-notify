#!/usr/bin/env python3

import argparse
import json
import os
import base64
from email.mime.text import MIMEText

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools
from apiclient.discovery import build
from apiclient import errors
from httplib2 import Http

from utils.logger import logger
from utils.endpoint import Endpoint

MAIL_SUBJECT = 'Notification from duty-notify'
CONFIG_FILE = 'config.json'
CLIENT_ID_FILE = 'client_id.json'
CREDENTIALS_FILE = 'credentials'
ENDPOINTS = [
    Endpoint('http://mail.stmarks.edu.hk/~smssmf/morning.htm', 'Morning'),
    Endpoint('http://mail.stmarks.edu.hk/~smssmf/assembly.htm', 'Assembly')
]

OAUTH2_SCOPES = 'https://www.googleapis.com/auth/gmail.send'


def main():
    logger.info('Started.')

    gmail = build('gmail', 'v1', http=make_google())
    gmail_send = gmail.users().messages().send
    email_messages = {}

    map(lambda x: x.request(), ENDPOINTS)

    with open(CONFIG_FILE, 'r') as file:
        users = json.load(file)
    logger.debug('User loaded')

    for endpoint in ENDPOINTS:
        logger.debug('Processing endpoint: %s', endpoint.name)
        endpoint.request()
        for user in users:
            logger.debug('Processing user: %s', user['name'])
            if user['name'] in endpoint:
                logger.debug('User in endpoint!')
                message = make_message('match', regexp=user['name'],
                                       name=endpoint.name, url=endpoint.url)
                email_messages.setdefault(user['email'], []).append(message)

    logger.debug('Done fetching endpoints. Now send email.')

    queue = []
    for recepient, messages in email_messages.items():
        message_text = make_message('frame', matches='\n'.join(messages))
        message = MIMEText(message_text)
        message['to'] = recepient
        # message['from'] = sender
        message['subject'] = MAIL_SUBJECT

        # The byte/str drama, you know.
        raw = base64.b64encode(message.as_string().encode())
        queue.append({'raw': raw.decode()})

    logger.debug(queue)

    consume_message_queue(gmail_send, queue)
    logger.info('Done.')


def make_google():
    """
    Request for credentials from Google OAuth2.
    After request, save them into credentials file.

    return -- httplib2 http object with Google OAuth2 authorized.
    """
    storage = Storage(CREDENTIALS_FILE)
    creds = storage.get()

    if not creds or creds.invalid:

        parser = argparse.ArgumentParser(parents=[tools.argparser])
        flags = parser.parse_args()

        flow = flow_from_clientsecrets(CLIENT_ID_FILE,
                                       scope=OAUTH2_SCOPES)
        flow.params['access_type'] = 'offline'
        creds = tools.run_flow(flow, storage, flags)
        storage.put(creds)

    return creds.authorize(Http())


def make_message(template, **kwargs):
    """
    Create a message from template.

    :param str template -- Template name that is under template directory,
    while template file must be ended with '.txt' suffex and passed in param
    does not.
    :param ** kwargs -- args that will be passed to str.format.

    :return str -- Rendered message.
    """
    with open(os.path.join('templates', template + '.txt'), 'r') as file:
        content = file.read()

    return content.format(**kwargs)


def consume_message_queue(send, queue):
    for message in queue:
        try:
            send(userId='me', body=message).execute()
        except errors.HttpError as error:
            logger.fatal('Error when sending a message. Error: %s', error)

if __name__ == "__main__":
    main()
