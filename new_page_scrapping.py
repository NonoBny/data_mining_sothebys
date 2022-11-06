import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import requests
from bs4 import BeautifulSoup

def get_path():
    path_option = int(input("Noa press 1 for you selenium driver path.\nYosef press 2 for yours\n"))
    if path_option == 1:
        _path = '/Users/nonobny/Desktop/Scolaire/ITC/Data_Mining_Sothebys/Selenium_Driver/chromedriver'
        return _path

    elif path_option == 2:
        _path = ''
        os.environ['PATH'] += r"C:/Users/josep/Desktop/SeleniumDrivers"
        return _path


def log_in_authentication():
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='LinkedText']//a[text()='Log In']"))).click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='form-input-row ']//input[@id='email']"))).send_keys(
        "noabenayoun1998@gmail.com")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                "//div[@class='form-input-row-password \n                        ']//input[@id='password']"))).send_keys(
        "itcnbVC5678")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='login-button-id']"))).click()


# each of our paths work differently
path = get_path()
if path != '':
    driver = webdriver.Chrome(path)
else:
    driver = webdriver.Chrome()

# Optional argument,
# if not specified will search path.
driver.get('https://www.sothebys.com/en/buy/auction/2022/monochrome-important-chinese-art')

# login in authentication will call the login function
log_in_authentication()

# access the list of results
hoverable_header = WebDriverWait(driver, 20)\
    .until(EC.element_to_be_clickable((By.XPATH, "//div[@class='PageHeader-body']")))

ActionChains(driver)\
        .move_to_element(hoverable_header)\
        .perform()
hoverable_auction = WebDriverWait(driver, 20)\
    .until(EC.element_to_be_clickable((By.XPATH, "//div[@class='PageHeader-body']//div[@class='NavigationItemTitle']//span[text()='Auctions']")))

ActionChains(driver)\
        .move_to_element(hoverable_auction)\
        .perform()

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='SothebysTopNavigationItem']//div[@class='NavigationLink']//a[text()='Results']"))).click()

different_sales = driver.find_elements(By.CLASS_NAME, "Card-info-container")
print(len(different_sales))

ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
for different_sale in different_sales:
    WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)\
        .until(EC.element_to_be_clickable(different_sale)).click()
    driver.back()
    print("testing\n")

#print([my_elem.get_attribute("textContent") for my_elem in driver.find_elements(By.CLASS_NAME, "SearchModule-results-item")])

"""
    for different_sale in different_sales:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='Card-info']//a[@class='Card-info-container']"))).click()
        different_sales = different_sales[1:]
        driver.back()
"""