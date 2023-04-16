import os
import shutil
import zipfile
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io

# Google Drive API 配置
SERVICE_ACCOUNT_FILE = 'secure/sevice_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

# 数据库配置
DB_BACKUP_NAME = 'D:/TempFiles/backup_ELE.json'
DB_NAME = 'db.sqlite3'

def download_latest_backup():
    # 创建一个Google Drive API客户端
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    try:
        # 查找备份文件
        query = "mimeType='application/zip' and trashed = false"
        results = service.files().list(q=query, fields="nextPageToken, files(id, name, createdTime)").execute()
        items = results.get('files', [])

        if not items:
            print('No backup files found.')
            return None
        else:
            # 按创建时间排序，获取最新的备份文件
            latest_backup = sorted(items, key=lambda x: x['createdTime'], reverse=True)[0]
            print(f"Latest backup: {latest_backup['name']} (ID: {latest_backup['id']})")

            # 下载备份文件
            request = service.files().get_media(fileId=latest_backup['id'])
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download progress: {int(status.progress() * 100)}.")
            
            # 解压备份文件
            file.seek(0)
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extract(DB_BACKUP_NAME)
            
            print("Backup downloaded and extracted successfully.")
            return True

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def restore_database():
    # 检查备份文件是否存在
    if not os.path.exists(DB_BACKUP_NAME):
        print("Backup file not found. Downloading the latest backup...")
        success = download_latest_backup()
        if not success:
            print("Failed to download the latest backup.")
            return

    # 用备份文件替换当前数据库
    restored_db_path = 'restored_db.sqlite3'
    shutil.copy2(DB_BACKUP_NAME, restored_db_path)
    print("Database restored successfully.")

if __name__ == "__main__":
    restore_database()
