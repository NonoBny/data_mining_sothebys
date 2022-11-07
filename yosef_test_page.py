from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import Sale
import requests
from bs4 import BeautifulSoup


# todo convert a sale to a sale object
# todo get all sales from all scrollable pages not just the first 15 on the first page
# todo get all items in a different_sale and continue with the rest of different_sales

WAIT_TIME = 20  # WAIT_TIME will be set here and used when we need it


def login():
    # login in authentification
    x_path_link = "//div[@class='LinkedText']//a[text()='Log In']"
    WebDriverWait(driver, WAIT_TIME)\
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link)))\
        .click()

    x_path_link = "//div[@class='form-input-row ']" \
                  "//input[@id='email']"

    text = "josephaschoen@gmail.com"

    WebDriverWait(driver, WAIT_TIME)\
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link)))\
        .send_keys(text)

    x_path_link = "//div[@class='form-input-row-password \n                        ']//input[@id='password']"

    text = "ITCDataMining22"
    WebDriverWait(driver, WAIT_TIME)\
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link)))\
        .send_keys(text)

    x_path_link = "//button[@id='login-button-id']"
    WebDriverWait(driver, WAIT_TIME)\
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link)))\
        .click()


def go_to_Results():
    x_path_link = "//div[@class='PageHeader-body']"
    hoverable_header = WebDriverWait(driver, WAIT_TIME)\
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link)))

    ActionChains(driver) \
        .move_to_element(hoverable_header) \
        .perform()

    x_path_link = "//div[@class='PageHeader-body']" \
                  "//div[@class='NavigationItemTitle']" \
                  "//span[text()='Auctions']"

    hoverable_auction = WebDriverWait(driver, WAIT_TIME)\
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link)))

    ActionChains(driver) \
        .move_to_element(hoverable_auction) \
        .perform()

    x_path_link = "//div[@class='SothebysTopNavigationItem']" \
                  "//div[@class='NavigationLink']" \
                  "//a[text()='Results']"

    WebDriverWait(driver, WAIT_TIME)\
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link)))\
        .click()


def get_sales():
    sales_list = []
    different_sales = []

    for i in range(10):
        different_sales_on_page = driver.find_elements(By.CLASS_NAME, "Card-info-container")

        for different_sale in different_sales_on_page:
            collection_page_link = different_sale.get_attribute('href')
            print(collection_page_link)
            driver2 = webdriver.Chrome()
            driver2.get(collection_page_link)
            print("jumped to a new link")
            driver2.close()
            print("returned back")

        different_sales = different_sales + different_sales_on_page

        link_to_next_page = driver.find_element(By.CLASS_NAME, "SearchModule-nextPageUrl")\
            .find_element(By.TAG_NAME, 'a')\
            .get_attribute('href')

        print(link_to_next_page)
        driver.get(link_to_next_page)
    print("end test2")

    print('number of sales: ' + str(len(different_sales)))
    for different_sale in different_sales:
        print(different_sale)
        sale = Sale.Sale(different_sale)
        sales_list.append(sale)
    return sales_list


if __name__ == '__main__':
    os.environ['PATH'] += 'C:/Users/josep/Desktop/SeleniumDrivers'  # adds the selenium Chrome Driver to my path
    driver = webdriver.Chrome()
    link = 'https://www.sothebys.com/en/buy/auction/2022/monochrome-important-chinese-art'
    driver.get(link)  # the url of the page we will start with

    login()  # will navigate to the login page and send the required information to log in
    go_to_Results()  # will navigate to the results page
    sales = get_sales()  # will get a list of all the sales on the results page



"""

"""