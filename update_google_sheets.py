import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# Google Sheets Credentials
SPREADSHEET_ID = "12GV03kPBdZhIOYKaT0_Nc5GASND4WaQnHmvFTIkbvWw"  # Replace with your actual Google Sheets ID
CREDENTIALS_FILE = "google_sheets_credentials.json"

# Authenticate and connect to Google Sheets
creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(creds)

# Load the sheet
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Read data from CSV
df = pd.read_csv("search_results.csv")

# Convert to list format for Google Sheets
data_list = df.values.tolist()

# Update Google Sheets
sheet.clear()
sheet.append_row(["Company Name", "Website", "Address", "Emails", "Phones"])
for row in data_list:
    sheet.append_row(row)

print("✅ Google Sheets updated successfully!")
