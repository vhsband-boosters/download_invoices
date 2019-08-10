from __future__ import print_function
import pickle
import os.path
import argparse
import sys
from pprint import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.transport.requests import AuthorizedSession

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
          'https://www.googleapis.com/auth/drive.readonly']
INVOICES_FOLDER_ID = '14vbrVAxA5h8r5TYz9YdeFBd3Ra342D5_'

# def args_parser():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-r', '--report', help="Report mode, displays differences", action="store_true")
#     parser.add_argument('-g', '--generate',
#                         help="Generate mode, generates missing mailing list entries as an import CSV",
#                         action="store_true")
#     return parser

def load_credentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def build_google_api(service, version):
    creds = load_credentials()
    svc = build(service, version, credentials=creds)
    return svc

def list_invoices():
    drive = build_google_api('drive', 'v3')

    dl = False
    page_token = None
    while True:
        resp = drive.files().list(q="'{0}' in parents and trashed = false".format(INVOICES_FOLDER_ID), spaces='drive',
                                fields='nextPageToken, files(id, name)', pageToken=page_token).execute()        
        for file in resp.get('files', []):
            print("Processing student {0}".format(file.get('name')))
            if file.get('name').startswith("Brown"):
                print("Starting downloads")
                dl = True
            if dl:
                name = file.get('name')
                filename = name.replace(", ", "_") + ".pdf"
                spreadsheetId = file.get('id')
                sheetsApi = build_google_api('sheets', 'v4')
                sheet = sheetsApi.spreadsheets().get(spreadsheetId=spreadsheetId, fields='spreadsheetUrl').execute()
                pprint(sheet)
                sheetUrl = sheet.get('spreadsheetUrl')
                action = 'export?exportFormat=pdf&format=pdf&portrait=false'
                dlUrl = sheetUrl.replace("edit", "") + action
                creds = load_credentials()
                session = AuthorizedSession(creds)
                dlResponse = session.get(dlUrl)
                with open("invoices/" + filename, 'wb') as f:
                    f.write(dlResponse.content)
            # print("File {0} id {1}".format(file.get('name'), file.get('id')))
        page_token = resp.get('nextPageToken')
        if page_token is None:
            break

def main():
    list_invoices()

if __name__ == '__main__':
    main()
