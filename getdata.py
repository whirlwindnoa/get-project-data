import time
import asyncio

from urllib.parse import quote_plus
from lxml import etree
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

xpaths = {
    "project_title": '//*[@id="__layout"]/div/div/header/div/div/div[1]/ol/li[2]/span',

    "popup_project_stats": '//*[@id="post-modal___BV_modal_body_"]/div[5]/div'
}

def fetchdata(id):
    driver.get(f"https://hub.kodland.org/ru/project/{id}")

    # wait until the page gets loaded and retrieve the title
    # shouldn't take longer than 10 seconds
    title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpaths["project_title"]))
    )
    time.sleep(1)
    name = title.get_attribute('innerHTML')

    # check whether the project gets a popup with statistics or not
    # usually works with most of the projects
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpaths["popup_project_stats"]))
        )
    except TimeoutException:
        driver.get(f"https://hub.kodland.org/ru/search?search={quote_plus(name)}")

    soup = bs(driver.page_source, features='lxml')

    stats = soup.find('div', class_="d-flex justify-content-between")
    if stats is not None:
        stats = stats.find_all('span', class_="stat__number")
    else:
        return None

    data = {
        "Name": name, 
        "Likes": 0,
        "Comments": 0,
        "Shares": 0,
        "Favorites": 0,
        "Views": 0
    }
    
    # fill out the data massive
    for x, stat in enumerate(stats):
        data[list(data.keys())[x+1]] = stat.text

    return data