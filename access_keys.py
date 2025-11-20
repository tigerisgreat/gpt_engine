import gspread
from google.oauth2.service_account import Credentials
import os
import json
import base64  # ADD THIS
from dotenv import load_dotenv
from datetime import datetime
import time
from utils import *
import random



load_dotenv()

SHEET_NAME = os.getenv("SHEET_NAME", "ChatGPT_Accounts")

def get_sheet():
    """Connect to Google Sheet using credentials from .env or env vars"""
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    
    # Get base64 encoded private key from GitHub Actions
    private_key_b64 = os.getenv("GOOGLE_PRIVATE_KEY_B64")
    
    if private_key_b64:
        # Decode from base64 (GitHub Actions)
        private_key = base64.b64decode(private_key_b64).decode()
    else:
        # Fall back to environment variable (local .env)
        private_key = os.getenv("GOOGLE_PRIVATE_KEY")
        if private_key and '\\n' in private_key:
            private_key = private_key.replace('\\n', '\n')
    
    creds_dict = {
        "type": "service_account",
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
        "private_key": private_key,
        "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "universe_domain": "googleapis.com"
    }
    
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1


# Get an available email id, make is_in_use=TRUE
def get_available_account():
    debug()
    num = random.randint(3, 180)
    print(f"Waiting {num} seconds before picking an account.")
    time.sleep(num)
    
    """Get first available account"""
    sheet = get_sheet()
    records = sheet.get_all_records()
    
    for i, record in enumerate(records):
        if str(record['is_in_use']).upper() == 'FALSE':
            row_num = i + 2
            sheet.update_cell(row_num, 4, 'TRUE')
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format: YYYY-MM-DD HH:MM:SS
            sheet.update_cell(row_num, 5, now)  # Write date/time in column 5
            print(f"[ACCESS-KEY] Got account: {record['email']}")
            return {
                'row': row_num,
                'index': record['index'],
                'email': record['email'],
                'password': record['password']
            }
    
    print("[ACCESS-KEYS] No available accounts!")
    return None

# Get password of a particular account
def get_password(email):
    """
    Get password for a specific account by email
    
    Args:
        email (str): Email address of the account
    
    Returns:
        str: Password if found
        None: If account not found
    
    Example:
        password = get_password("test@example.com")
    """
    sheet = get_sheet()
    
    try:
        records = sheet.get_all_records()
        for record in records:
            if record['email'] == email:
                password = record['password']
                print(f"::notice::[ACCESS-KEYS] Retrieved password for: {email}")
                return password
        
        print(f"::error::[ACCESS-KEYS] Email not found: {email}")
        return None
        
    except Exception as e:
        print(f"::error::[ACCESS-KEYS] Error getting password: {e}")
        return None


# Updates the password of a given account
def update_password(email, new_password):
    """Update password by email"""
    sheet = get_sheet()
    records = sheet.get_all_records()
    
    for i, record in enumerate(records):
        if record['email'] == email:
            row_num = i + 2
            sheet.update_cell(row_num, 3, new_password)
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format: YYYY-MM-DD HH:MM:SS
            sheet.update_cell(row_num, 6, now)  # Write date/time in column 5
            print(f"::notice::[ACCESS-KEYS] Updated password for: {email}")
            return True
    
    print(f"::error::[ACCESS-KEYS] Email not found: {email}")
    return False

# Release an account, make is_in_use=FALSE
def release_account(email=None):
    """
    Mark account as free (is_in_use = FALSE)
    Uses only email to identify the account.
    Example: release_account(email="test@example.com")
    """
    sheet = get_sheet()
    
    if not email:
        print("::error::[Error ACCESS-KEYS] Must provide email")
        return False
    
    records = sheet.get_all_records()
    for i, record in enumerate(records):
        if record['email'] == email:
            row_num = i + 2  # +2 because row 1 is header
            sheet.update_cell(row_num, 4, 'FALSE')
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format: YYYY-MM-DD HH:MM:SS
            sheet.update_cell(row_num, 7, now)  # Write date/time in column 5
            print(f"[ACCESS-KEYS] Released account: {email} (row {row_num})")
            return True
    
    print(f"[ACCESS-KEYS] Email not found: {email}")
    return False


# Resets all account make is_in_use to is_in_use=FALSE for all accounts
def reset_all_accounts():
    """Reset all accounts to FREE"""
    sheet = get_sheet()
    records = sheet.get_all_records()
    for i in range(len(records)):
        sheet.update_cell(i + 2, 4, 'FALSE')
    print("[ACCESS-KEYS] All accounts reset to FREE")


