import gspread
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials
from django.conf import settings
import os
from django.http import JsonResponse
import json

def fetch_student_data():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = os.path.join(settings.STATICFILES_DIRS[0], 'credentials.json')

    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)

    SHEET_ID = '1XDLMKIxssigi58ch7mxahauzqODo3ot4NuDXrgqCnww'
    WORKSHEET_NAME = 'details'

    sheet = client.open_by_key(SHEET_ID).worksheet(WORKSHEET_NAME)
    student_data = sheet.get_all_records()

    return student_data