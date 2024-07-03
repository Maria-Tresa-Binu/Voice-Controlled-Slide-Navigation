from google import Create_Service
from googleapiclient.http import MediaFileUpload 

CLIENT_SECRET_FILE = 'client-secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# Specify the file to upload
file_name = r'C:\Users\Maria Tresa Binu\Downloads\malasian budget.xlsx'  # Replace with the actual path of your file

# Create file metadata
file_metadata = {'name': 'Malaysian budget'}  # Change the name as needed

# Upload the file to Google Drive
media = MediaFileUpload(file_name, resumable=True)
file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

print(f'File uploaded! File ID: {file.get("id")}')


