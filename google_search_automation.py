from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# Function to extract emails and phone numbers from a website
def extract_emails_and_phones(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        emails = set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", soup.text))
        phones = set(re.findall(r"\+?\d[\d -]{8,14}\d", soup.text))

        return list(emails), list(phones)
    except:
        return [], []

# Function to scrape Google Search results
def google_search_and_maps(query, max_pages=20):
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    results = []
    for _ in range(max_pages):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for g in soup.find_all('div', class_='tF2Cxc'):
            try:
                link = g.find('a')['href']
                title = g.find('h3').text if g.find('h3') else "No Title"
                emails, phones = extract_emails_and_phones(link)
                results.append([title, link, "", ", ".join(emails), ", ".join(phones)])
            except:
                continue

        # Try to go to the next page
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next")
            next_button.click()
            time.sleep(3)
        except:
            break

    driver.quit()
    return results

# Run the script
search_query = "Spices Exporters in India"
print(f"🔍 Searching for: {search_query}")
data = google_search_and_maps(search_query)

# Save data to CSV
df = pd.DataFrame(data, columns=["Company Name", "Website", "Address", "Emails", "Phones"])
df.to_csv("search_results.csv", index=False)
print("✅ Data saved to search_results.csv")
