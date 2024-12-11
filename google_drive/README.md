# Google Drive Integration

This module provides utilities for interacting with Google Drive.

## Setup

1. Create a Google Cloud Project and enable the Google Drive API
2. Create OAuth 2.0 credentials and download the `client_secret.json` file
3. Place the `client_secret.json` file in this directory
4. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```python
from google_drive.drive_utils import upload_file, list_files, download_file

# Upload a file
file_id = upload_file('example.txt', 'text/plain')

# List files
files = list_files()
for file in files:
    print(f'Name: {file["name"]}, ID: {file["id"]}')

# Download a file
download_file(file_id, 'downloaded_example.txt')
```

## Security Notes

- Never commit `client_secret.json` or `token.pickle` to version control
- Store these files securely
- Use environment variables for sensitive information

## Error Handling

The functions will raise exceptions for common errors:
- `FileNotFoundError`: When client_secret.json is missing
- `google.auth.exceptions.RefreshError`: When credentials are invalid
- `googleapiclient.errors.HttpError`: For API-related errors

Implement try-except blocks as needed in your application.