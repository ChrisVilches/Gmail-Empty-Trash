from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from util import Util

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']
SENDER_PATTERNS_FILENAME = './sender_patterns.txt'


def get_messages_from_trash(messages_client):
    results = messages_client.list(userId='me', maxResults=5,
                                   labelIds=['TRASH']).execute()
    msgs = results.get('messages', [])
    return list(map(lambda m: messages_client.get(userId='me', id=m['id']).execute(), msgs))


def filter_using_patterns(messages, patterns):
    result = []
    for msg in messages:
        msg_from = filter(
            lambda hdr: hdr['name'] == 'From', msg['payload']['headers'])
        msg_from = list(msg_from)[0]

        if Util.substring_of_any(msg_from['value'], patterns):
            result.append(msg)
    return result


def create_messages_client():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080, open_browser=False)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service.users().messages()


def read_sender_patterns_file():
    try:
        return Util.file_lines_to_set(SENDER_PATTERNS_FILENAME)

    except FileNotFoundError as error:
        print('Error: File {0} must exist'.format(SENDER_PATTERNS_FILENAME))
        print(error)
        exit()


def main():
    messages_client = create_messages_client()
    sender_patterns = read_sender_patterns_file()

    if not sender_patterns:
        print(SENDER_PATTERNS_FILENAME, 'is empty. Exiting.')
        return

    try:
        trash_messages = get_messages_from_trash(messages_client)
        filtered_msgs = filter_using_patterns(trash_messages, sender_patterns)

        ignored = len(trash_messages) - len(filtered_msgs)

        print('Messages:', len(filtered_msgs), 'Ignored:', ignored)

        if not filtered_msgs:
            return

        msg_ids = list(map(lambda m: m['id'], filtered_msgs))

        print(msg_ids)
        messages_client.batchDelete(
            userId='me', body={'ids': msg_ids}).execute()
        print('OK ({0} removed)'.format(len(msg_ids)))

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
