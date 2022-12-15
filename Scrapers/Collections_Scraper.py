import argparse
import json
import sys
import textwrap
import time
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup
from currency_converter import CurrencyConverter
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from Sothebys_Objects.Sothebys_Objects import Collection, Item, ArtPiece


with open('config.json') as config_file:
    data = json.load(config_file)

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

def login() -> None:
    """login to authenticate"""

    WebDriverWait(driver, data['WAIT_TIME_20']) \
        .until(EC.element_to_be_clickable((By.XPATH, data['X_PATH_LINK_1']))) \
        .click()

    file = open('password_id', mode='r')
    text_1 = file.readline().strip()

    WebDriverWait(driver, data['WAIT_TIME_20']) \
        .until(EC.element_to_be_clickable((By.XPATH, data['X_PATH_LINK_2']))) \
        .send_keys(text_1)

    text_2 = file.readline().strip()

    WebDriverWait(driver, data['WAIT_TIME_20']) \
        .until(EC.element_to_be_clickable((By.XPATH, data['X_PATH_LINK_3']))) \
        .send_keys(text_2)

    WebDriverWait(driver, data['WAIT_TIME_20']) \
        .until(EC.element_to_be_clickable((By.XPATH, data['X_PATH_LINK_4']))) \
        .click()


def go_to_results() -> None:
    """get to the result page of the sothebys website"""

    hoverable_header = WebDriverWait(driver, data['WAIT_TIME_20']) \
        .until(EC.element_to_be_clickable((By.XPATH, data['X_PATH_LINK_5'])))

    ActionChains(driver) \
        .move_to_element(hoverable_header) \
        .perform()

    hoverable_auction = WebDriverWait(driver, data['WAIT_TIME_20']) \
        .until(EC.element_to_be_clickable((By.XPATH, data['X_PATH_LINK_6'])))

    ActionChains(driver) \
        .move_to_element(hoverable_auction) \
        .perform()

    WebDriverWait(driver, data['WAIT_TIME_20']) \
        .until(EC.element_to_be_clickable((By.XPATH, data['X_PATH_LINK_7']))) \
        .click()


def get_url_n_sale_total() -> Tuple[List[str], List[str]]:
    """get all the links and the total sale amount for each collection on the result page"""
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    time.sleep(data['WAIT_TIME_20'])

    list_url: List[str] = []
    list_sale_total: List[str] = []
    sale_items = soup.find_all('a', class_=data['SALE_IT_ELE'], href=True)

    for sale_item in sale_items:
        if data['AUCTION_LINK'] in sale_item['href']:
            list_url.append(str(sale_item['href']))
            total_sale_list = sale_item.find("div", class_=data['TOTAL_SALE_ELE'])
            if not total_sale_list:
                total_sale_str = data['NA_INFO']
            else:
                total_sale = total_sale_list.text.split()
                if not total_sale:
                    total_sale_str = data['NA_INFO']
                else:
                    total_sale_str = total_sale[2].replace(",", "") + " " + total_sale[3]
            list_sale_total.append(total_sale_str)
    return list_url, list_sale_total


def get_info_string(item) -> str:
    return data['NA_INFO'] if item is None else item[0].text


def general_info() -> Tuple[str, str, str, str]:
    """to get 4 data points from the page : title, date, time and location"""
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    document_object_model = etree.HTML(str(soup))
    results = soup.find("h1", class_=data['RESULT_FOR_SOUP'])
    date_auction = document_object_model.xpath(data['DATE_AUCT'])
    time_auction = document_object_model.xpath(data['TIME_AUCT'])
    location_auction = document_object_model.xpath(data['LOC_AUCT'])

    str_date = get_info_string(date_auction)
    str_loc = get_info_string(location_auction)

    if time is None:
        str_time = data['NA_INFO']
    else:
        str_time = time_auction[0]

    return results.text, str_date, str_time, str_loc


def get_item_data(sale_item: BeautifulSoup, tag_type: str, class_name: str) -> Tuple[str, str, str]:
    """get the index, info and type of item"""
    item_obj = sale_item.find(tag_type, class_=class_name)
    type_of_item = data['OTHER_ITEMS']
    if item_obj is not None:
        info_title = item_obj.text.split(maxsplit=1)
        index = info_title[0][:-1]
        title = info_title[1]
        return index, title, type_of_item
    return '', '', type_of_item


def get_art_display_data(sale_item: BeautifulSoup, author_tag_type: str, author_class_name: str,
                         title_tag_type: str, title_class_name: str) -> Tuple[str, str, str, str]:
    author_and_index = sale_item.find(author_tag_type, class_=author_class_name)
    title_art = sale_item.find(title_tag_type, class_=title_class_name)
    type_of_item = data['ART_PIECES']
    if author_and_index is not None and title_art is not None:
        author_and_index = author_and_index.text.split(maxsplit=1)
        index = author_and_index[0][:-1]
        author = author_and_index[1]
        title = title_art.text
        return index, title, type_of_item, author
    return '', '', type_of_item, ''


def get_item_or_art_display_data(sale_item: BeautifulSoup) -> Tuple[str, ...]:
    if sale_item.find("p", class_=data['SALE_ITEM_FIND']) is not None:
        return get_item_data(sale_item, "p", data['SALE_ITEM_FIND'])

    if sale_item.find("div", class_=data['SALE_ART_FIND']) is not None:
        return get_art_display_data(sale_item, "p", data['SALE_ART_DATA_1'], "p", data['SALE_ART_DATA_2'])

    if sale_item.find("p", class_=data['SALE_ART_DATA']):
        author_class_name = data['SALE_ART_AUTHOR']
        title_class_name = data['SALE_ART_TITLE']
        return get_art_display_data(sale_item, "h5", author_class_name, "p", title_class_name)

    else:
        return get_item_data(sale_item, "h5", data['SALE_ITEM_TITLE'])


def check_data_none(price_sold, reserve_item, estimate_price) -> Tuple[str, str, str, str]:
    """verify if the data point are available or not (for example in case of ongoing auction"""
    if price_sold is not None:
        price_info = price_sold.text.split()
        price_number = int(price_info[0].replace(",", ""))
        price_currency = price_info[1]
    else:
        price_number = data['NOT_SOLD']
        price_currency = data['NA_INFO']

    if reserve_item is not None:
        reserve_or_not = reserve_item.text
    else:
        reserve_or_not = data['RESERVE']

    if estimate_price is not None:
        estimate_price_str = estimate_price.text.replace(",", "")
    else:
        estimate_price_str = data['NO_EST_AV']

    return price_number, price_currency, reserve_or_not, estimate_price_str


def get_collection_item_data(soup: BeautifulSoup, square_or_list_class_name: str, price_sold_class_name: str,
                             estimated_price_class_name: str, reserve_item_class_name: str) \
        -> Tuple[List[Item], Dict[str, int]]:
    items: List[Item] = []
    count_dict: Dict[str, int] = {data['ART_PIECES']: 0, data['OTHER_ITEMS']: 0}

    sale_items_list = soup.find_all('div', class_=square_or_list_class_name)

    for sale_item in sale_items_list:
        item_data = get_item_or_art_display_data(sale_item)
        index = item_data[0]
        author = ''
        title = item_data[1]
        item_type = item_data[2]
        if len(item_data) == 4:
            author = item_data[3]

        price_sold = sale_item.find("p", class_=price_sold_class_name)
        estimate_price = sale_item.find_all("p", class_=estimated_price_class_name)[1]
        reserve_item = sale_item.find("p", class_=reserve_item_class_name)

        price_number, price_currency, reserve_or_not, estimate_price_str = \
            check_data_none(price_sold, reserve_item, estimate_price)

        if item_type == data['OTHER_ITEMS']:
            item = Item(index, title, price_number, price_currency, reserve_or_not, estimate_price_str)
        else:
            item = ArtPiece(index, author, title, price_number, price_currency,
                            reserve_or_not, estimate_price_str)
        count_dict[item.type] += 1

        items.append(item)

    return items, count_dict


def get_collection_data() -> Collection:
    """get all the items data point in addition to general info and specific info (art or object)
      so we get the selling price, estimated price, currency used, reserve or not and return a dictionary
      for the collection"""
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(data['WAIT_TIME_5'])
    gen_info = general_info()

    number_items = soup.find('p', class_=data['NUM_ITEMS']).text.split()[0]

    sale_items_list = soup.find_all('div', class_=data['SALE_ITEM_LIST'])
    if sale_items_list is not None:
        sale_items_class_name = data['SALE_ITEM_FORMAT_1']
        price_sold_class_name = data['PRICE_SOLD_FORMAT_1']
        estimate_price_class_name = data['ESTIMATE_PRICE_FORMAT_1']
        reserve_item_class_name = data['RESERVE_FORMAT_1']

    else:
        sale_items_class_name = data['SALE_ITEM_FORMAT_2']
        price_sold_class_name = data['PRICE_SOLD_FORMAT_2']
        estimate_price_class_name = data['ESTIMATE_PRICE_FORMAT_2']
        reserve_item_class_name = data['RESERVE_FORMAT_2']

    items, count_dict = get_collection_item_data(soup, sale_items_class_name, price_sold_class_name,
                                                 estimate_price_class_name, reserve_item_class_name)

    type_of_items = max(count_dict, key=count_dict.get)
    collection = Collection(gen_info, number_items, type_of_items, items)
    return collection


def get_page_data(list_links, list_total_sales) -> List[Collection]:
    data_point_list: List[Collection] = []

    for link in list_links:
        driver.get(link)
        try:
            collection = get_collection_data()
            collection.total_sale = list_total_sales.pop(0)
            try:
                args = parser_for_scraper()
                if args.notsold:
                    collection.print_gen_info()
                    collection.print_item_not_sold()
                elif args.typeitem is not None:
                    type_item = args.typeitem
                    collection.print_type_item(type_item)
                elif args.totalsale is not None:
                    total_sale = args.totalsale
                    try:
                        price_point = int(total_sale[0])
                        currency = total_sale[1]
                        c = CurrencyConverter()
                        if currency not in c.currencies:
                            raise ValueError
                        else:
                            collection.print_coll_total_sale_min(price_point, currency)
                    except ValueError:
                        print("Either the 1st parameter is not an integer, or the currency you've "
                              "entered is wrong")
                        sys.exit(1)
                else:
                    collection.print_gen_info()
                    collection.print_item_info()
                data_point_list.append(collection)
            except SystemExit:
                print('Something is wrong with the arguments you have passed on the terminal !')
                driver.quit()
                sys.exit(1)
        except IndexError:
            continue
    return data_point_list


def get_result_page_data() -> List[Collection]:
    """final dictionary data list"""
    data_point_list: List[Collection] = []
    link_to_next_page = data['LINK_NEXT_RES']

    for page_number in range(data['NUMBER_OF_PAGES'] - 1):
        list_links, list_total_sales = get_url_n_sale_total()
        data_point_list += get_page_data(list_links, list_total_sales)
        driver.get(link_to_next_page)
        link_to_next_page = driver.find_element(By.CLASS_NAME, data['NEXT_PAGE_URL']) \
            .find_element(By.TAG_NAME, 'a').get_attribute('href')
        driver.get(link_to_next_page)

    driver.quit()

    return data_point_list


def parser_for_scraper():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent(
                                         ''' Three different actions can be taken through the parser :
        * you can print only the unsold items
         [--notsold] 
        * you can choose which type of items between 
        {'Other items', 'Art pieces'} you would like to print"
         [--typeitem {Other items,Art pieces}]
        * you can set a minimum total sale value in any currency 
        you want and to only print the auctions with a total sale above it, 
        whatever is the currency they were sold in
        [--totalsale number currency]'''))
    parser.add_argument('--notsold', action='store_true',
                        help='Action that calls only the items that were not sold')
    parser.add_argument('--typeitem', type=str, choices=['Other items', 'Art pieces'],
                        help='Action that has to be followed with the type of item desired between "" to only '
                             'print the collection with this specific type of item', default=None)
    parser.add_argument('--totalsale', nargs=2, type=str, metavar=('number', 'currency'),
                        help="Action to print the collection total sale price value above the number "
                             "you are entering and given the currency entered (to be able to compare it to"
                             " collections sold in other currencies)", default=None)

    parsed_arguments = parser.parse_args()
    return parsed_arguments


def main() -> List[Collection]:
    """initialize the driver, login and get the info"""
    driver.get(data['START_LINK'])
    login()
    go_to_results()
    result_page_data = get_result_page_data()
    print(len(result_page_data))
    return result_page_data


if __name__ == '__main__':
    main()
