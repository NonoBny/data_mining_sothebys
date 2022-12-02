from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import json
from typing import List
from Sothebys_Objects.Sothebys_Objects import Place

with open('config.json') as config_file:
    data = json.load(config_file)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


# todo need to implement
def main() -> List[Place]:
    return []


#class_="UnevenTwoColumnContainer-columnOne"


