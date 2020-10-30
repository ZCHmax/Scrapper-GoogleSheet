from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_binary
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from google.oauth2.service_account import Credentials
from datetime import date


# Grab Result
driver = webdriver.Chrome()
driver.get('https://www.google.com/search?&q=site:instagram.com+linkfol.io')

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

tag = soup.find("div", class_="appbar")
result = str(tag.text.split(' ')[1]).replace(',', '')


# Write to Google Sheet
json_key = json.load(open('creds.json'))
scopes = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_info(json_key, scopes=scopes)
file = gspread.authorize(credentials)
sheet = file.open("Test Auto Daily Scrapper").sheet1

f_date = date(2020, 10, 28)
l_date = date.today()
d = (l_date - f_date).days
sheet.update_cell(d+1, 1, str(l_date))
sheet.update_cell(d+1, 2, result)
