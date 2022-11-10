import time

from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

WAIT_TIME = 20
START_LINK = 'https://www.sothebys.com/en/'
AUCTION_LINK = 'https://www.sothebys.com/en/buy/auction/'
NUMBER_OF_PAGES = 2

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def login():
    """login to authentificate"""

    x_path_link = "//div[@class='LinkedText']//a[text()='Log In']"
    WebDriverWait(driver, WAIT_TIME) \
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link))) \
        .click()

    x_path_link = "//div[@class='form-input-row ']" \
                  "//input[@id='email']"

    text = "josephaschoen@gmail.com"

    WebDriverWait(driver, WAIT_TIME) \
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link))) \
        .send_keys(text)

    x_path_link = "//div[@class='form-input-row-password \n                        ']//input[@id='password']"

    text = "ITCDataMining22"
    WebDriverWait(driver, WAIT_TIME) \
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link))) \
        .send_keys(text)

    x_path_link = "//button[@id='login-button-id']"
    WebDriverWait(driver, WAIT_TIME) \
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link))) \
        .click()


def item_or_art_display_list(sale_item):
    """check if the auction is of art pieces (with an author) or antiques/objects etc
    because data points are not the same in this case (no author) and return the specific data points
    if the display is in list form"""
    # this is when it is an art production (3 data points)
    if sale_item.find("p", class_="css-1o7cmk8"):
        item_obj = sale_item.find("p", class_="css-1o7cmk8")
        if item_obj is not None:
            info_title = item_obj.text.split(maxsplit=1)
            index_item = info_title[0][:-1]
            title_item = info_title[1]
            type_item = "Other items"
        return index_item, title_item, type_item
    # this is when it is an object (2 data points)
    if sale_item.find("div", class_="css-wdkl43"):
        author_and_index = sale_item.find("p", class_="css-8908nx")
        title_art = sale_item.find("p", class_="css-17ei96f")
        if author_and_index is not None and title_art is not None:
            author_and_index = author_and_index.text.split(maxsplit=1)
            index = author_and_index[0][:-1]
            author = author_and_index[1]
            title_of_artpiece = title_art.text
            type_item = "Art pieces"
        return index, title_of_artpiece, author, type_item


def item_or_art_display_square(sale_item):
    """check if the auction is of art pieces (with an author) or antiques/objects etc
        because data points are not the same in this case (no author) and return the specific data points
        if the display is in square form"""
    # this is when it is an art production (3 data points)
    if sale_item.find("p", class_="paragraph-module_paragraph16Regular__CXt6G css-5dbuiq"):
        author_and_index = sale_item.find("h5", class_="headline-module_headline20Regular__zmXrx css-y1q8mr")
        title_art = sale_item.find("p", class_="paragraph-module_paragraph14Regular__Zfr98 css-17r6vaq")
        if author_and_index is not None and title_art is not None:
            author_and_index = author_and_index.text.split(maxsplit=1)
            index = author_and_index[0][:-1]
            author = author_and_index[1]
            title_of_artpiece = title_art.text
            type_item = "Art pieces"
        return index, title_of_artpiece, author, type_item
    # this is when it is an object (2 data points)
    else:
        item_obj = sale_item.find("h5", class_="headline-module_headline20Regular__zmXrx css-1t5w3xl")
        if item_obj is not None:
            info_title = item_obj.text.split(maxsplit=1)
            index_item = info_title[0][:-1]
            title_item = info_title[1]
            type_item = "Other items"
        return index_item, title_item, type_item


def check_type_display(happy_souping):
    """check the type of display (list or square)"""
    if not happy_souping:
        return False
    else:
        return True


def lenght_type_type(type_item, collect_dict, estimate_price_str, price_number, price_currency, reserve_or_not):
    if len(type_item) == 4:
        collect_dict["Type of items"] = type_item[3]
        new_dict = {"Title of Item": type_item[1], "Author": type_item[2], "Estimated Price": estimate_price_str,
                    "Selling price": price_number, "Currency": price_currency, "Reserve": reserve_or_not}
    # check if it is an item (with 2 data points title and index)
    elif len(type_item) == 3:
        collect_dict["Type of Items"] = type_item[2]
        new_dict = {"Title of Item": type_item[1], "Estimated Price": estimate_price_str,
                    "Selling price": price_number, "Currency": price_currency, "Reserve": reserve_or_not}
    else:
        new_dict = {}
    return new_dict


def check_data_none(price_sold, reserve_item, estimate_price):
    if price_sold is not None:
        price_info = price_sold.text.split()
        price_number = price_info[0]
        price_currency = price_info[1]
    else:
        price_number = "not sold"
        price_currency = "n/a"

    if reserve_item is not None:
        reserve_or_not = reserve_item.text
    else:
        reserve_or_not = "reserve"

    if estimate_price is not None:
        estimate_price_str = estimate_price.text
    else:
        estimate_price_str = "No estimation available"

    return price_number, price_currency, reserve_or_not, estimate_price_str


def get_collection_data():
    """get all the items data point in addition to general info and specific info (art or object)
      so we get the selling price, estimated price, currency used, reserve or not and return a dictionary
      for the collection"""
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(5)
    #gen_info = general_info()

    collect_dict = {}

    number_items = soup.find('p', class_="paragraph-module_paragraph14Regular__Zfr98 css-ccdn7j")
    number_item_str = number_items.text.split()[0]
    collect_dict["Number of items"] = number_item_str
    dict_items = {}
    sale_items = soup.find_all('div', class_='css-1up9enl')

    # if the display is a list
    if check_type_display(sale_items):
        # get the selling price, estimated price, currency used, reserve for each item
        for sale_item in sale_items:
            it = item_or_art_display_list(sale_item)
            price_sold = sale_item.find("p", class_="label-module_label12Medium__THkRn css-2r8rz8")
            estimate_price = sale_item.find_all("p", class_="paragraph-module_paragraph14Regular__Zfr98 css-trd9wg")[1]
            reserve_item = sale_item.find("p", class_="label-module_label12Medium__THkRn css-1hu9w0v")

            price_number, price_currency, reserve_or_not, estimate_price_str = check_data_none(price_sold, reserve_item, estimate_price)

            # check if it is a art work (with 3 data points title, author and index)
            # or an item (with 2 data points title and index) and return the data
            new_dict = lenght_type_type(it, collect_dict, estimate_price_str,
                                        price_number, price_currency, reserve_or_not)

            dict_items[it[0]] = new_dict

    # if the display is made up of 'square'
    else:
        sale_items_2 = soup.find_all('div', class_="css-1esu0b4")
        # get the selling price, estimated price, currency used, reserve for each item
        for sale_item in sale_items_2:
            it = item_or_art_display_square(sale_item)
            price_sold = sale_item.find("p", class_="label-module_label14Medium__uD9e- css-l21c39")
            estimate_price = sale_item.find_all("p", class_="paragraph-module_paragraph14Regular__Zfr98 css-trd9wg")[1]
            # TODO i think it is the class for the list, need to check
            reserve_item = sale_item.find("p", class_="label-module_label12Medium__THkRn css-1xkt3wv")

            price_number, price_currency, reserve_or_not, estimate_price_str = check_data_none(price_sold, reserve_item,
                                                                                               estimate_price)

            new_dict = lenght_type_type(it, collect_dict, estimate_price_str,
                                        price_number, price_currency, reserve_or_not)

            dict_items[it[0]] = new_dict

    collect_dict["Items"] = dict_items
    return collect_dict


if __name__ == '__main__':
    driver.get(START_LINK)
    login()
    driver.get("https://www.sothebys.com/en/buy/auction/2022/classic-design?locale=en")
    time.sleep(10)

    print(get_collection_data())
