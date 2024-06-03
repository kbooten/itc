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

import time

def append_data_to_google_sheet(values, service=service, range_name='interactions!A1'):
    try:
        body = {'values': values}
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheetId, range=range_name,
            valueInputOption='RAW', body=body).execute()
        print(f"{result.get('updates').get('updatedCells')} cells appended.")
    except Exception as e:
        print(f"Error appending data to Google Sheet: {e}")

def write_field_to_google_sheets():
    try:
        with open('_field_prose_.txt', 'r') as f:
            field_prose = f.read()
        with open('_field_yaml_.txt', 'r') as f:
            field_yaml = f.read()
        info_to_write = [[int(time.time()), field_prose, field_yaml]]
        append_data_to_google_sheet(info_to_write, range_name='updated_field!A1')
        print("Wrote rooms to Google Sheets")
    except Exception as e:
        print(f"Error writing field to Google Sheets: {e}")


def main():
    write_field_to_google_sheets()

if __name__ == '__main__':
    main()