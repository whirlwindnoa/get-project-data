import time
import asyncio
from urllib.parse import quote_plus

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

def document_initialised(driver):
    return driver.execute_script("return initialised")

def fetchdata(id):
    driver.get(f"https://hub.kodland.org/ru/project/{id}")

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="post-modal___BV_modal_body_"]/div[1]/h3'))
        )
    except TimeoutException:
        pass

    soup = bs(driver.page_source, features='lxml')
    
    el = None
    try:
        el = driver.find_element(By.XPATH, '//*[@id="post-modal___BV_modal_body_"]/div[5]/div/div[2]/span')
    except:
        el = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/header/div/div/div[1]/ol/li[2]/span')
        name = el.text
    
        driver.get(f"https://hub.kodland.org/ru/search?search={quote_plus(name)}")

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div/div[2]/div[2]/div/div/div/div[2]/div'))
        )
        soup = bs(driver.page_source, features="lxml")

    stats = soup.find('div', class_="d-flex justify-content-between")
    stats = stats.find_all('span', class_="stat__number")

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