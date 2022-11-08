from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import copy

import requests
from bs4 import BeautifulSoup

# constants

WAIT_TIME = 20
START_LINK = 'https://www.sothebys.com/en'
proper_sale_link = 'https://www.sothebys.com/en/buy/auction/'


def login(which_driver, x_path_link):
    # login in authentification
    WebDriverWait(which_driver, WAIT_TIME) \
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link))) \
        .click()

    x_path_link = "//div[@class='form-input-row ']" \
                  "//input[@id='email']"

    text = "noabenayoun1998@gmail.com"

    WebDriverWait(which_driver, WAIT_TIME) \
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link))) \
        .send_keys(text)

    x_path_link = "//div[@class='form-input-row-password \n                        ']//input[@id='password']"

    text = "itcnbVC5678"
    WebDriverWait(which_driver, WAIT_TIME) \
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link))) \
        .send_keys(text)

    x_path_link = "//button[@id='login-button-id']"
    WebDriverWait(which_driver, WAIT_TIME) \
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link))) \
        .click()

def get_data_from_sale_page():
    html = driver.page_source
    soup = BeautifulSoup(html)
    results = soup.find("div", class_="css-1i2uczc")
    sale_items = results.find_all("div", class_="css-m0n40v")
    for sale_item in sale_items:
        title_item = sale_item.find("p", class_="css-1o7cmk8")
        print(title_item)


def go_to_Results():
    x_path_link = "//div[@class='PageHeader-body']"
    hoverable_header = WebDriverWait(driver, WAIT_TIME) \
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link)))

    ActionChains(driver) \
        .move_to_element(hoverable_header) \
        .perform()

    x_path_link = "//div[@class='PageHeader-body']" \
                  "//div[@class='NavigationItemTitle']" \
                  "//span[text()='Auctions']"

    hoverable_auction = WebDriverWait(driver, WAIT_TIME) \
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link)))

    ActionChains(driver) \
        .move_to_element(hoverable_auction) \
        .perform()

    x_path_link = "//div[@class='SothebysTopNavigationItem']" \
                  "//div[@class='NavigationLink']" \
                  "//a[text()='Results']"

    WebDriverWait(driver, WAIT_TIME) \
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link))) \
        .click()


def get_sales():
    for i in range(10):
        different_sales_on_page = driver.find_elements(By.CLASS_NAME, "Card-info-container")
        for different_sale in different_sales_on_page:
            collection_page_link = different_sale.get_attribute('href')
            # check if the sale page is in proper format for data scrapping (for example not catalogue or sometime)
            # TODO maybe turn it into a function check or something
            if collection_page_link is not None and proper_sale_link in collection_page_link:
                print(collection_page_link)
                driver2 = webdriver.Chrome('/Users/nonobny/Desktop/Scolaire/ITC/Data_Mining_Sothebys/chromedriver')
                driver2.get(START_LINK)
                login(driver2, "//div[@class='LinkedText']//a[text()='Log In']")
                driver2.get(collection_page_link)

                print("jumped to a new link")
                driver2.close()
                print("returned back")

        link_to_next_page = driver.find_element(By.CLASS_NAME, "SearchModule-nextPageUrl") \
            .find_element(By.TAG_NAME, 'a') \
            .get_attribute('href')

        print(link_to_next_page)
        driver.get(link_to_next_page)
    print("end test2")


if __name__ == '__main__':
    driver = webdriver.Chrome(
        '/Users/nonobny/Desktop/Scolaire/ITC/Data_Mining_Sothebys/chromedriver')  # Optional argument,
    # if not specified will search path.

    driver.get(START_LINK)  # the url of the page we will start with

    login(driver, "//div[@class='LinkedText']//a[text()='Log In']")  # will navigate to the login page and send the required information to log in
    go_to_Results()  # will navigate to the results page
    get_sales()
