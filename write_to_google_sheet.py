import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

import time

# Get the current Unix timestamp
current_timestamp = int(time.time())

# Get the JSON string from the environment variable
creds_json_string = os.getenv('GOOGLE_CREDS')

# Convert string back to JSON
creds_json = json.loads(creds_json_string)

# Use credentials to create a service account object
creds = service_account.Credentials.from_service_account_info(creds_json)

service = build('sheets', 'v4', credentials=creds)

def append_data_to_google_sheet(values, service=service, range_name='Sheet1!A1'):
    body = {
        'values': values
    }
    result = service.spreadsheets().values().append(
        spreadsheetId="1_vH-JFTVr7VN6kKd0U_eJ7XEsRXvqOQ1vr9Eu-ciGSY", range=range_name,
        valueInputOption='RAW', body=body).execute()
    print('{0} cells appended.'.format(result \
                                       .get('updates') \
                                       .get('updatedCells')))

data_to_append = [["example user id","example user input", "example reply",int(time.time())],]
append_data_to_google_sheet(data_to_append)