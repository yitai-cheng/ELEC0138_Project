import os
import pickle
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from django.conf import settings
from django.core.management import call_command
from celery import shared_task
import logging
import tempfile

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
token_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token.pickle')

# Load Google Drive API credentials
with open(token_file_path, 'rb') as token:
    creds = pickle.load(token)

# Initialize Google Drive API client
service = build('drive', 'v3', credentials=creds, cache_discovery=False)

@shared_task
def backup_data_to_google_drive():

    logging.info('Starting backup_data_to_google_drive task')
   
    # Create a temporary file to store the database backup
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_dir = tempfile.gettempdir()
    backup_path = os.path.join(temp_dir, f"backup_{now}.json")
    call_command('dumpdata', 'mysite', output=backup_path)

    file_metadata = {
        'name': backup_path,
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
