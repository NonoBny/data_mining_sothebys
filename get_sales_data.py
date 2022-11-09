from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from lxml import etree
from main import list_items

# constants

WAIT_TIME = 20
START_LINK = 'https://www.sothebys.com/en'

#variable
data_point_list = []

# initialize driver

driver = webdriver.Chrome(
    '/Users/nonobny/Desktop/Scolaire/ITC/Data_Mining_Sothebys/chromedriver')


def login(which_driver):
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


def general_info():
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    documentobjectmodel = etree.HTML(str(soup))
    results = soup.find("h1", class_="headline-module_headline48Regular__oAvHN css-liv8gb")
    date = documentobjectmodel.xpath("//*[@id='__next']/div/div[4]/div/div[1]/div[4]/div/div[2]/div/p[1]")
    time = documentobjectmodel.xpath("//*[@id='__next']/div/div[4]/div/div[1]/div[4]/div/div[2]/div/p[1]/text()[2]")
    location = documentobjectmodel.xpath("//*[@id='__next']/div/div[4]/div/div[1]/div[4]/div/div[2]/div/p[2]")
    if date is None:
        str_date = "n/a"
    else:
        str_date = date[0].text
    if time is None:
        str_time = "n/a"
    else:
        str_time = time[0]
    if location is None:
        str_loc = "n/a"
    else:
        str_loc = location[0].text

    return results.text, str_date, str_time, str_loc

# is it objects or art production (with an author)
def item_or_art(sale_item):
    if sale_item.find("p", class_="css-1o7cmk8"):
        item_obj = sale_item.find("p", class_="css-1o7cmk8")
        if item_obj is not None:
            info_title = item_obj.text.split(maxsplit=1)
            index_item = info_title[0][:-1]
            title_item = info_title[1]
        return index_item, title_item
    if sale_item.find("div", class_="css-wdkl43"):
        author_and_index = sale_item.find("p", class_="css-8908nx")
        title_art = sale_item.find("p", class_="css-17ei96f")
        if author_and_index is not None and title_art is not None:
            author_and_index = author_and_index.text.split(maxsplit=1)
            index = author_and_index[0][:-1]
            author = author_and_index[1]
            title_of_artpiece = title_art.text
        return index, title_of_artpiece, author

def item_or_art_display_square(sale_item):
    if sale_item.find("p", class_="paragraph-module_paragraph16Regular__CXt6G css-5dbuiq"):
        author_and_index = sale_item.find("h5", class_="headline-module_headline20Regular__zmXrx css-y1q8mr")
        title_art = sale_item.find("p", class_="paragraph-module_paragraph14Regular__Zfr98 css-17r6vaq")
        print(author_and_index, title_art)
        if author_and_index is not None and title_art is not None:
            author_and_index = author_and_index.text.split(maxsplit=1)
            index = author_and_index[0][:-1]
            author = author_and_index[1]
            title_of_artpiece = title_art.text
        return index, title_of_artpiece, author
    else:
        item_obj = sale_item.find("h5", class_="headline-module_headline20Regular__zmXrx css-17r6vaq")
        print(item_obj)
        if item_obj is not None:
            info_title = item_obj.text.split(maxsplit=1)
            index_item = info_title[0][:-1]
            title_item = info_title[1]
        return index_item, title_item


def get_collection_data():
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    gen_info = general_info()
    collect_dict = {"Title of Collection": gen_info[0], "Date of Auction": gen_info[1],
                    "Time of Auction": gen_info[2], "Place of Auction": gen_info[3]}
    #sale_items = soup.find_all('div', class_='css-1up9enl')
    sale_items = soup.find_all('div', class_="css-1esu0b4")
    print(check_type_display(sale_items))

    dict_items = {}
    for sale_item in sale_items:
        print(sale_item.find("h5", class_="headline-module_headline20Regular__zmXrx css-17r6vaq"))
        it = item_or_art(sale_item)
        price_sold = sale_item.find("p", class_="label-module_label12Medium__THkRn css-2r8rz8")
        estimate_price = sale_item.find_all("p", class_="paragraph-module_paragraph14Regular__Zfr98 css-trd9wg")[1]
        reserve_item = sale_item.find("p", class_="label-module_label12Medium__THkRn css-1hu9w0v")
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
        estimate_price_str = estimate_price.text

        if len(it) == 3:
            new_dict = {"Title of Item": it[1], "Author": it[2], "Estimated Price": estimate_price_str,
                        "Selling price": price_number, "Currency": price_currency, "Reserve": reserve_or_not}
        elif len(it) == 2:
            new_dict = {"Title of Item": it[1], "Estimated Price": estimate_price_str,
                        "Selling price": price_number, "Currency": price_currency, "Reserve": reserve_or_not}

        dict_items[it[0]] = new_dict

    collect_dict["Items:"] = dict_items
    return collect_dict

def trying_to_find():
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    sale_items = soup.find_all('div', class_="css-1esu0b4")
    for sale_item in sale_items:
        it = item_or_art_display_square(sale_item)
        print(it)
        price_sold = sale_item.find("p", class_="label-module_label14Medium__uD9e- css-l21c39")
        estimate_price = sale_item.find_all("p", class_="paragraph-module_paragraph14Regular__Zfr98 css-trd9wg")[1]
        reserve_item = sale_item.find("p", class_="label-module_label12Medium__THkRn css-1xkt3wv")
        print(price_sold, estimate_price, reserve_item)
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
        estimate_price_str = estimate_price.text

        if len(it) == 3:
            new_dict = {"Title of Item": it[1], "Author": it[2], "Estimated Price": estimate_price_str,
                            "Selling price": price_number, "Currency": price_currency, "Reserve": reserve_or_not}
        elif len(it) == 2:
            new_dict = {"Title of Item": it[1], "Estimated Price": estimate_price_str,
                            "Selling price": price_number, "Currency": price_currency, "Reserve": reserve_or_not}

        #dict_items[it[0]] = new_dict

def check_type_display(happy_souping):
    if not happy_souping:
        return False
    else:
        return True


if __name__ == '__main__':
    driver.get(
        'https://www.sothebys.com/en/buy/auction/2022/classic-design?locale=en')
    button = WebDriverWait(driver, WAIT_TIME) \
        .until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id='__next']/div/div[4]/div/div[1]/div[4]/div/div[4]/div/div/button[1]")))

    button.click()
    login(driver)

    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    sale_items = soup.find_all('div', class_="css-1esu0b4")
    for sale_item in sale_items:
        print(item_or_art_display_square(sale_item))
    trying_to_find()
"""    general_info()
    get_collection_data()

"""

