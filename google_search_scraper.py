import time
import re
import requests
import gspread
from bs4 import BeautifulSoup
from google.oauth2.service_account import Credentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Google Sheets API setup
SERVICE_ACCOUNT_FILE = "google_sheets_credentials.json"
SPREADSHEET_ID = "12GV03kPBdZhIOYKaT0_Nc5GASND4WaQnHmvFTIkbvWw"
  # Replace with your actual spreadsheet ID

# Authenticate with Google Sheets
scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Function to extract emails and phone numbers from a website
def extract_emails_and_phones(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        emails = list(set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup.text)))
        phones = list(set(re.findall(r"\+?\d[\d\s\-\(\)]{7,}\d", soup.text)))

        return emails, phones
    except:
        return [], []

# Function to scrape Google Search
def google_search(query, max_results=5):
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    results = []

    for g in soup.find_all('div', class_='tF2Cxc')[:max_results]:
        link = g.find('a')['href']
        title = g.find('h3').text if g.find('h3') else "No Title"
        emails, phones = extract_emails_and_phones(link)
        results.append([title, link, ', '.join(emails), ', '.join(phones)])

    driver.quit()
    return results

# Main function to scrape Google and save data
def main():
    search_query = "Best coffee shops in New York"  # Modify this query as needed
    data = google_search(search_query)

    sheet.update("A1", [["Business Name", "Website", "Emails", "Phones"]] + data)
    print("✅ Data successfully added to Google Sheets!")

if __name__ == "__main__":
    main()
