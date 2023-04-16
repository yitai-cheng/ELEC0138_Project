import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
SCOPES = ['https://www.googleapis.com/auth/drive']

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

with open('token.pickle', 'wb') as token:
    pickle.dump(creds, token)