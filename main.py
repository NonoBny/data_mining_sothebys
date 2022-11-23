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
NUMBER_OF_PAGES = 10

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def login():
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


def go_to_results():
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


def get_url_n_sale_total():
    """get all the links and the total sale amount for each collection on the result page"""
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(20)
    list_url = []
    list_sale_total = []
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


#######################################################

def general_info():
    """to get 4 data points from the page : title, date, time and location"""
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    documentobjectmodel = etree.HTML(str(soup))
    results = soup.find("h1", class_="headline-module_headline48Regular__oAvHN css-liv8gb")
    date_auction = documentobjectmodel.xpath("//*[@id='__next']/div/div[4]/div/div[1]/div[4]/div/div[2]/div/p[1]")
    time_auction = documentobjectmodel.xpath(
        "//*[@id='__next']/div/div[4]/div/div[1]/div[4]/div/div[2]/div/p[1]/text()[2]")
    location_auction = documentobjectmodel.xpath("//*[@id='__next']/div/div[4]/div/div[1]/div[4]/div/div[2]/div/p[2]")

    def get_info_string(item):
        return 'n/a' if item is None else item[0].text

    str_date = get_info_string(date_auction)
    str_loc = get_info_string(location_auction)

    if time is None:
        str_time = "n/a"
    else:
        str_time = time_auction[0]

    return results.text, str_date, str_time, str_loc


# is it objects or art production (with an author) in case of list display
def item_or_art_display_list(sale_item):
    """check if the auction is of art pieces (with an author) or antiques/objects etc
    because data points are not the same in this case (no author) and return the specific data points
    if the display is in list form"""

    if sale_item.find("p", class_="css-1o7cmk8"):
        item_obj = sale_item.find("p", class_="css-1o7cmk8")

        if item_obj is not None:
            info_title = item_obj.text.split(maxsplit=1)
            index_item = info_title[0][:-1]
            title_item = info_title[1]
            type_item = "Other items"
        return index_item, title_item, type_item

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
    return happy_souping


def length_type_type(type_item, count_dict, estimate_price_str, price_number, price_currency, reserve_or_not):
    """check which type of items are being sold (art pieces or other items) and
    return the appropriate dictionary of data depending on the type of item for each item
    return also the count of type of items bc sothebys people did confusing things sometime so few items could
    pass for the other type but we need to know which type of items is the most reccuring type
    bc it is going to be the right one"""
    if len(type_item) == 4:
        count_dict[type_item[3]] += 1
        new_dict = {"Title of Item": type_item[1], "Author": type_item[2], "Estimated Price": estimate_price_str,
                    "Selling price": price_number, "Currency": price_currency, "Reserve": reserve_or_not}
    elif len(type_item) == 3:
        count_dict[type_item[2]] += 1
        new_dict = {"Title of Item": type_item[1], "Estimated Price": estimate_price_str,
                    "Selling price": price_number, "Currency": price_currency, "Reserve": reserve_or_not}
    else:
        new_dict = {}
    return new_dict, count_dict


def check_data_none(price_sold, reserve_item, estimate_price):
    """verify if the data point are available or not (for exemple in case of ungoing auction"""
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


def max_type_items(count_dict):
    """return the max out of two dictionary, is going to be used for the type of items """
    return max(count_dict, key=count_dict.get)


def get_collection_data():
    """get all the items data point in addition to general info and specific info (art or object)
      so we get the selling price, estimated price, currency used, reserve or not and return a dictionary
      for the collection"""
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(5)
    gen_info = general_info()

    collect_dict = {"Title of Collection": gen_info[0], "Date of Auction": gen_info[1],
                    "Time of Auction": gen_info[2], "Place of Auction": gen_info[3]}

    number_items = soup.find('p', class_="paragraph-module_paragraph14Regular__Zfr98 css-ccdn7j")
    number_item_str = number_items.text.split()[0]
    collect_dict["Number of items"] = number_item_str

    dict_items = {}
    count_dict = {'Art pieces': 0, 'Other items': 0}
    sale_items = soup.find_all('div', class_='css-1up9enl')

    if check_type_display(sale_items):
        for sale_item in sale_items:
            it = item_or_art_display_list(sale_item)
            price_sold = sale_item.find("p", class_="label-module_label12Medium__THkRn css-2r8rz8")
            estimate_price = sale_item.find_all("p", class_="paragraph-module_paragraph14Regular__Zfr98 css-trd9wg")[1]
            reserve_item = sale_item.find("p", class_="label-module_label12Medium__THkRn css-1hu9w0v")

            price_number, price_currency, reserve_or_not, estimate_price_str = check_data_none(price_sold, reserve_item,
                                                                                               estimate_price)

            new_dict, count_dict = length_type_type(it, count_dict, estimate_price_str,
                                                    price_number, price_currency, reserve_or_not)

            dict_items[it[0]] = new_dict

    else:
        sale_items_2 = soup.find_all('div', class_="css-1esu0b4")
        for sale_item in sale_items_2:
            it = item_or_art_display_square(sale_item)
            price_sold = sale_item.find("p", class_="label-module_label14Medium__uD9e- css-l21c39")
            estimate_price = sale_item.find_all("p", class_="paragraph-module_paragraph14Regular__Zfr98 css-trd9wg")[1]
            reserve_item = sale_item.find("p", class_="label-module_label12Medium__THkRn css-1xkt3wv")

            price_number, price_currency, reserve_or_not, estimate_price_str = check_data_none(price_sold, reserve_item,
                                                                                               estimate_price)

            new_dict, count_dict = length_type_type(it, count_dict, estimate_price_str,
                                                    price_number, price_currency, reserve_or_not)

            dict_items[it[0]] = new_dict

    type_of_items = max_type_items(count_dict)
    collect_dict["Type of Items"] = type_of_items
    collect_dict["Items"] = dict_items
    return collect_dict


def get_result_page_data():
    """final dictionary data list"""
    data_point_list = []
    link_to_next_page = "https://www.sothebys.com/en/results?locale=en"
    page_index = 0

    for page_number in range(NUMBER_OF_PAGES - 1):
        list_links, list_total_sales = get_url_n_sale_total()

        for link in list_links:
            driver.get(link)
            general_info()
            each_coll_dictionary = get_collection_data()
            print(each_coll_dictionary)
            data_point_list.append(each_coll_dictionary)

        index = 0
        while index < (len(list_total_sales) - 1):
            data_point_list[index + page_index]["Total Sale"] = list_total_sales[index]
            index += 1
        page_index += 1
        driver.get(link_to_next_page)
        link_to_next_page = driver.find_element(By.CLASS_NAME, "SearchModule-nextPageUrl") \
            .find_element(By.TAG_NAME, 'a').get_attribute('href')
        driver.get(link_to_next_page)

    driver.quit()

    return data_point_list


def main():
    """initialize the driver, login and get the info"""
    driver.get(START_LINK)
    login()
    go_to_results()
    print(get_result_page_data())


if __name__ == '__main__':
    main()
