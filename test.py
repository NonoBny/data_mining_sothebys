import os
from selenium.webdriver import Chrome

os.environ['PATH'] += r"C:/Users/josep/Desktop/SeleniumDrivers"
driver = Chrome()
driver.get('https://www.sothebys.com/en/buy/auction/2022/monochrome-important-chinese-art')
