#!/bin/python3

import os
import googleapiclient.http
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = "./credentials.json"

def create_folder(name: str):
	creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
	service = build('drive', 'v3', credentials=creds)

	file_metadata = {
		"name": name,
		"mimeType": "application/vnd.google-apps.folder",
	}

	file = service.files().create(body=file_metadata, fields="id").execute()
	print(f'Folder ID: "{file.get("id")}".')
	return file.get("id")

def list_files():
	creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
	service = build('drive', 'v3', credentials=creds)

	results = (
		service.files()
		.list(pageSize=10, fields="nextPageToken, files(id, name)")
		.execute()
	)
	items = results.get("files", [])

	if not items:
		print("No files found.")
		return
	print("Files:")
	for item in items:
		print(f"{item['name']} ({item['id']})")

def upload_file(file_path: str, folder_id: str) -> str:
	creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
	service = build('drive', 'v3', credentials=creds)

	file_metadata = {
		'name': os.path.basename(file_path),
		'parents': [folder_id]
	}
	media = googleapiclient.http.MediaFileUpload(file_path, resumable=True)
	uploaded_file = service.files().create(
		body=file_metadata,
		media_body=media,
		fields='id'
	).execute()

	print(f"File uploaded with ID: {uploaded_file['id']}")
	return uploaded_file['id']


def delete_file(file_id: str):
	creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
	service = build('drive', 'v3', credentials=creds)
	response = service.files().delete(fileId=file_id).execute()

def delete_all_files():
	sure = input("Are you sure? (y): ")
	if sure != "y": return

	creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
	service = build('drive', 'v3', credentials=creds)

	results = (
		service.files()
		.list(pageSize=10, fields="nextPageToken, files(id, name)")
		.execute()
	)
	items = results.get("files", [])

	for file in items:
		service.files().delete(fileId=file['id']).execute()

def allow_read(file_id: str):
	creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
	service = build('drive', 'v3', credentials=creds)

	body = {
		"type": "anyone",
		"role": "reader",
	}
	response = service.permissions().create(
		fileId=file_id,
		body=body,
		fields="id",
	).execute()

def get_folder_id(folder_name: str, new_folder_allow_read = True):
	"""Gets the id of the single folder with that name, otherwise makes that folder."""
	creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
	service = build('drive', 'v3', credentials=creds)

	results = service.files().list(q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false", fields="*").execute()

	items = results.get("files", [])

	if not items:
		print("No Folder of that name, Creating new folder.")
		folder_id = create_folder(folder_name)
		if new_folder_allow_read: allow_read(folder_id)
		return folder_id
	
	if len(items) > 1:
		raise RuntimeError("more than 1 folder of that name exists")
	
	return items[0]['id']


if __name__ == "__main__":
	folder_id = create_folder("testing")
	file_id = upload_file("./void2.png", folder_id)
	print("created files!!!")
	list_files()

	delete_file(folder_id)
	delete_file(file_id)
	print("deleted files!!!")
	list_files()
