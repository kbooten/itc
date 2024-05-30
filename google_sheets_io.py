import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build


# Get the JSON string from the environment variable
from dotenv import load_dotenv
load_dotenv()  # This will load environment variables from a .env file if present
creds_json_string = os.getenv('GOOGLE_CREDS')

# Convert string back to JSON
creds_json = json.loads(creds_json_string)

# Use credentials to create a service account object
creds = service_account.Credentials.from_service_account_info(creds_json)

service = build('sheets', 'v4', credentials=creds)

spreadsheetId="1_vH-JFTVr7VN6kKd0U_eJ7XEsRXvqOQ1vr9Eu-ciGSY"


import json

import os

def get_current_room_desc(room_id):
    module_dir = os.path.dirname(__file__)  # __file__ is a special variable of the module
    path_to_rooms = os.path.join(module_dir, 'prompt_text/rooms/')
    with open(path_to_rooms+room_id+".txt",'r') as f:
        room_desc = f.read()
    return room_desc


def append_data_to_google_sheet(values, service=service, range_name='interactions!A1'):
    body = {
        'values': values
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheetId, range=range_name,
        valueInputOption='RAW', body=body).execute()
    print('{0} cells appended.'.format(result \
                                       .get('updates') \
                                       .get('updatedCells')))


def write_field_to_google_sheets():
    import time
    with open('_field_prose_.txt','r') as f:
        field_prose = f.read()
    with open('_field_yaml_.txt','r') as f:
        field_yaml = f.read()
    info_to_write = [[int(time.time()),field_prose,field_yaml]]
    append_data_to_google_sheet(info_to_write,range_name='updated_field!A1')
    print("wrote rooms to google")


def main():
    write_field_to_google_sheets.write()

if __name__ == '__main__':
    main()