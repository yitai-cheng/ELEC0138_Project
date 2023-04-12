import os
import datetime
import pickle
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from django.conf import settings
from django.core.management import call_command
from celery import shared_task
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
token_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token.pickle')

# Load Google Drive API credentials
with open(token_file_path, 'rb') as token:
    creds = pickle.load(token)

# Initialize Google Drive API client
service = build('drive', 'v3', credentials=creds)

@shared_task
def backup_data_to_google_drive():

    logging.info('Starting backup_data_to_google_drive task')
    backup_file = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    backup_path = os.path.join('/tmp', backup_file)

    call_command('dumpdata', 'mysite', output=backup_path)

    file_metadata = {
        'name': backup_file,
        'mimeType': 'application/json',
    }

    try:
        media = MediaFileUpload(backup_path, mimetype='application/json')
        file = service.files().create(
            body=file_metadata, media_body=media, fields='id'
        ).execute()
        logging.info(f'File ID: "{file.get("id")}".')
    except HttpError as error:
        logging.error(f'An error occurred: {error}')
        file = None

    return file
