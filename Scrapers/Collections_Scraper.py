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
from typing import Dict, List, Tuple
import Collection

WAIT_TIME = 20
START_LINK = 'https://www.sothebys.com/en/'
AUCTION_LINK = 'https://www.sothebys.com/en/buy/auction/'
NUMBER_OF_PAGES = 20

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def login() -> None:
    """login to authentificate"""

    x_path_link = "//div[@class='LinkedText']//a[text()='Log In']"
    WebDriverWait(driver, WAIT_TIME) \
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link))) \
        .click()

    x_path_link = "//div[@class='form-input-row ']" \
                  "//input[@id='email']"

    file = open('password_id', mode='r')
    text = file.readline().strip()

    WebDriverWait(driver, WAIT_TIME) \
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link))) \
        .send_keys(text)

    x_path_link = "//div[@class='form-input-row-password \n                        ']//input[@id='password']"

    text = file.readline().strip()

    WebDriverWait(driver, WAIT_TIME) \
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link))) \
        .send_keys(text)

    x_path_link = "//button[@id='login-button-id']"
    WebDriverWait(driver, WAIT_TIME) \
        .until(EC.element_to_be_clickable((By.XPATH, x_path_link))) \
        .click()


def go_to_results() -> None:
    """get to the result page of the sothebys website"""
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


def get_url_n_sale_total() -> Tuple[List[str], List[str]]:
    """get all the links and the total sale amount for each collection on the result page"""
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(20)
    list_url: List[str] = []
    list_sale_total: List[str] = []
    sale_items = soup.find_all('a', class_='Card-info-container', href=True)
    for sale_item in sale_items:
        if AUCTION_LINK in sale_item['href']:
            list_url.append(str(sale_item['href']))
            total_sale_list = sale_item.find("div", class_="Card-salePrice")
            if not total_sale_list:
                total_sale_str = "n/a"
            else:
                total_sale = total_sale_list.text.split()
                if not total_sale:
                    total_sale_str = "n/a"
                else:
                    total_sale_str = total_sale[2] + " " + total_sale[3]
            list_sale_total.append(total_sale_str)
    return list_url, list_sale_total


def general_info() -> Tuple[str, str, str, str]:
    """to get 4 data points from the page : title, date, time and location"""
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    document_object_model = etree.HTML(str(soup))
    results = soup.find("h1", class_="headline-module_headline48Regular__oAvHN css-liv8gb")
    date_auction = document_object_model.xpath("//*[@id='__next']/div/div[4]/div/div[1]/div[4]/div/div[2]/div/p[1]")
    time_auction = document_object_model.xpath(
        "//*[@id='__next']/div/div[4]/div/div[1]/div[4]/div/div[2]/div/p[1]/text()[2]")
    location_auction = document_object_model.xpath("//*[@id='__next']/div/div[4]/div/div[1]/div[4]/div/div[2]/div/p[2]")

    get_info_string = lambda item: 'n/a' if item is None else item[0].text

    str_date = get_info_string(date_auction)
    str_loc = get_info_string(location_auction)

    if time is None:
        str_time = "n/a"
    else:
        str_time = time_auction[0]

    return results.text, str_date, str_time, str_loc


def get_item_data(sale_item: BeautifulSoup, tag_type: str, class_name: str) -> Tuple[str, str, str]:
    item_obj = sale_item.find(tag_type, class_=class_name)
    type_of_item = "Other items"
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
    type_of_item = "Art pieces"
    if author_and_index is not None and title_art is not None:
        author_and_index = author_and_index.text.split(maxsplit=1)
        index = author_and_index[0][:-1]
        author = author_and_index[1]
        title = title_art.text
        return index, title, type_of_item, author
    return '', '', type_of_item, ''


def get_item_or_art_display_data(sale_item: BeautifulSoup) -> Tuple[str, ...]:
    # this is when it is an art production (3 data points)
    if sale_item.find("p", class_="css-1o7cmk8"):
        return get_item_data(sale_item, "p", "css-1o7cmk8")

    # this is when it is an object (2 data points)
    if sale_item.find("div", class_="css-wdkl43"):
        return get_art_display_data(sale_item, "p", "css-8908nx", "p", "css-17ei96f")

    # this is when it is an art production (3 data points)
    if sale_item.find("p", class_="paragraph-module_paragraph16Regular__CXt6G css-5dbuiq"):
        author_class_name = "headline-module_headline20Regular__zmXrx css-y1q8mr"
        title_class_name = "paragraph-module_paragraph14Regular__Zfr98 css-17r6vaq"
        return get_art_display_data(sale_item, "h5", author_class_name, "p", title_class_name)

    # this is when it is an object (2 data points)
    else:
        return get_item_data(sale_item, "h5", "headline-module_headline20Regular__zmXrx css-1t5w3xl")


def check_data_none(price_sold, reserve_item, estimate_price) -> Tuple[str, str, str, str]:
    """verify if the data point are available or not (for example in case of ongoing auction"""
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


def get_collection_item_data(soup: BeautifulSoup, square_or_list_class_name: str, price_sold_class_name: str,
                             estimated_price_class_name: str, reserve_item_class_name: str)\
        -> Tuple[List[Collection.Item], Dict[str, int]]:

    items: List[Collection.Item] = []
    count_dict: Dict[str, int] = {'Art pieces': 0, 'Other items': 0}

    # if the display is a list
    sale_items_list = soup.find_all('div', class_=square_or_list_class_name)

    # get the selling price, estimated price, currency used, reserve for each item
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

        if item_type == "Other Items":
            item = Collection.Item(index, title, price_number, price_currency, reserve_or_not, estimate_price_str)
        else:
            item = Collection.ArtPiece(index, author, title, price_number, price_currency,
                                       reserve_or_not, estimate_price_str)
        count_dict[item.type] += 1

        items.append(item)

    return items, count_dict


def get_collection_data() -> Collection.Collection:
    """get all the items data point in addition to general info and specific info (art or object)
      so we get the selling price, estimated price, currency used, reserve or not and return a dictionary
      for the collection"""
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(5)
    gen_info = general_info()

    number_items = soup.find('p', class_="paragraph-module_paragraph14Regular__Zfr98 css-ccdn7j").text.split()[0]

    sale_items_list = soup.find_all('div', class_='css-1up9enl')
    if sale_items_list:
        sale_items_class_name = "css-1up9enl"
        price_sold_class_name = "label-module_label12Medium__THkRn css-2r8rz8"
        estimate_price_class_name = "paragraph-module_paragraph14Regular__Zfr98 css-trd9wg"
        reserve_item_class_name = "label-module_label12Medium__THkRn css-1hu9w0v"

    else:
        sale_items_class_name = "css-1esu0b4"
        price_sold_class_name = "label-module_label14Medium__uD9e- css-l21c39"
        estimate_price_class_name = "paragraph-module_paragraph14Regular__Zfr98 css-trd9wg"
        reserve_item_class_name = "label-module_label12Medium__THkRn css-1xkt3wv"

    items, count_dict = get_collection_item_data(soup, sale_items_class_name, price_sold_class_name,
                                                 estimate_price_class_name, reserve_item_class_name)

    type_of_items = max(count_dict, key=count_dict.get)
    collection = Collection.Collection(gen_info, number_items, type_of_items, items)
    return collection


def get_page_data(list_links, list_total_sales) -> List[Collection.Collection]:
    data_point_list: List[Collection.Collection] = []

    for link in list_links:
        driver.get(link)
        collection = get_collection_data()
        collection.total_sale = list_total_sales.pop(0)
        collection.print()
        data_point_list.append(collection)
    return data_point_list


def get_result_page_data() -> List[Collection.Collection]:
    """final dictionary data list"""
    data_point_list: List[Collection.Collection] = []
    link_to_next_page = "https://www.sothebys.com/en/results?locale=en"

    # for each result's result page
    for page_number in range(NUMBER_OF_PAGES - 1):
        list_links, list_total_sales = get_url_n_sale_total()
        data_point_list += get_page_data(list_links, list_total_sales)
        driver.get(link_to_next_page)
        link_to_next_page = driver.find_element(By.CLASS_NAME, "SearchModule-nextPageUrl") \
            .find_element(By.TAG_NAME, 'a').get_attribute('href')
        driver.get(link_to_next_page)

    driver.quit()

    return data_point_list


def main() -> List[Collection.Collection]:
    """initialize the driver, login and get the info"""
    driver.get(START_LINK)
    login()
    go_to_results()
    result_page_data = get_result_page_data()
    print(len(result_page_data))
    return result_page_data


if __name__ == '__main__':
    main()
