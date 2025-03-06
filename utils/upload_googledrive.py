import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

# Google Drive API 스코프 설정
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_drive_service():
    creds = None
    # if os.path.exists('token.json'):
    #     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('/workspace/VLMEvalKit/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)


def upload_to_drive(filename, folder_id=None):
    service = get_drive_service()
    file_metadata = {
        'name': filename,
        'parents': [folder_id]  # 특정 폴더에 업로드하기 위한 설정
    }
    if folder_id:
        file_metadata['parents'] = [folder_id]
    media = MediaFileUpload(filename, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"파일이 업로드되었습니다. 파일 ID: {file.get('id')}")

if __name__ == '__main__':
    # create_csv()
    folder_id = ["1DI-iRLHEqXYbcF8CQ1H8Hm40f0X7bC8u"]
    upload_to_drive('/workspace/VLMEvalKit/MMPB.tar.gz', folder_id)