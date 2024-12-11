from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os.path
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive():
    creds = None
    # Check if token exists from previous authentication
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials available, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def upload_file(filename, mimetype):
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)
    
    file_metadata = {'name': filename}
    media = MediaFileUpload(filename, mimetype=mimetype)
    
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    
    print(f'File ID: {file.get("id")}')
    return file.get('id')

def list_files():
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)
    
    results = service.files().list(
        pageSize=10, 
        fields="nextPageToken, files(id, name)"
    ).execute()
    
    items = results.get('files', [])
    return items

def download_file(file_id, output_filename):
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)
    
    request = service.files().get_media(fileId=file_id)
    with open(output_filename, 'wb') as f:
        f.write(request.execute())

def create_folder(folder_name):
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)
    
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    
    file = service.files().create(
        body=file_metadata,
        fields='id'
    ).execute()
    
    return file.get('id')

def share_file(file_id, email):
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)
    
    batch = service.new_batch_http_request()
    user_permission = {
        'type': 'user',
        'role': 'reader',
        'emailAddress': email
    }
    
    batch.add(service.permissions().create(
        fileId=file_id,
        body=user_permission,
        fields='id',
    ))
    
    batch.execute()