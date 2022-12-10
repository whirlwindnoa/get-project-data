import time
import asyncio

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

async def fetchdata(id):
    driver.get(f"https://hub.kodland.org/ru/project/{id}")

    soup = bs(driver.page_source, features='lxml')

    stats = soup.find_all('span', class_="stat__number")
    data = list()

    for stat in stats:
        await data.append(stat.text)

    return data