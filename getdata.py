import time
import asyncio
import urllib

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

def document_initialised(driver):
    return driver.execute_script("return initialised")

def fetchdata(id):
    driver.get(f"https://hub.kodland.org/ru/project/{id}")

    elem = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "stat__number"))
    )
    soup = bs(driver.page_source, features='lxml')
    try:
        el = driver.find_element(By.CLASS_NAME, "stat_number")
    except NoSuchElementException:
        el = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/header/div/div/div[1]/ol/li[2]/span')
        name = el.text
    
        driver.get(urllib.parse.quote_plus(f"https://hub.kodland.org/ru/search?search={name}"))

        WebDriverWait(driver, timeout=5).until(document_initialised)
        soup = bs(driver.page_source, features="lxml")

    stats = soup.find_all('span', class_="stat__number")
    data = {
        "Likes": 0,
        "Comments": 0,
        "Shares": 0,
        "Favorites": 0,
        "Views": 0
    }
    

    for x, stat in enumerate(stats):
        data[list(data.keys())[x]] = stat.text

    return data