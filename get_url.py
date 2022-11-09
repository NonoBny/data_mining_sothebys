import time

from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

WAIT_TIME = 20
START_LINK = 'https://www.sothebys.com/en/'
AUCTION_LINK = 'https://www.sothebys.com/en/buy/auction/'

driver = webdriver.Chrome(
    '/Users/nonobny/Desktop/Scolaire/ITC/Data_Mining_Sothebys/chromedriver')


def login():
    """login to authentificate"""
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


def get_url():
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(10)
    list_url = []
    sale_items = soup.find_all('a', class_='Card-info-container', href=True)
    for sale_item in sale_items:
        if AUCTION_LINK in sale_item['href']:
            list_url.append(str(sale_item['href']))
    return list_url

#######################################################


def general_info():
    """to get 4 data points from the page : title, date, time and location"""
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


# is it objects or art production (with an author) in case of list display
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
        return index_item, title_item
    # this is when it is an object (2 data points)
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
        return index, title_of_artpiece, author
    # this is when it is an object (2 data points)
    else:
        item_obj = sale_item.find("h5", class_="headline-module_headline20Regular__zmXrx css-17r6vaq")
        if item_obj is not None:
            info_title = item_obj.text.split(maxsplit=1)
            index_item = info_title[0][:-1]
            title_item = info_title[1]
        return index_item, title_item


def check_type_display(happy_souping):
    """check the type of display (list or square)"""
    if not happy_souping:
        return False
    else:
        return True


def get_collection_data():
    """get all the items data point in addition to general info and specific info (art or object)
      so we get the selling price, estimated price, currency used, reserve or not and return a dictionary
      for the collection"""
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(10)
    gen_info = general_info()
    collect_dict = {"Title of Collection": gen_info[0], "Date of Auction": gen_info[1],
                    "Time of Auction": gen_info[2], "Place of Auction": gen_info[3]}
    dict_items = {}
    sale_items = soup.find_all('div', class_='css-1up9enl')
    if check_type_display(sale_items):
        for sale_item in sale_items:
            it = item_or_art_display_list(sale_item)
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
    else:
        sale_items_2 = soup.find_all('div', class_="css-1esu0b4")
        for sale_item in sale_items_2:
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

            dict_items[it[0]] = new_dict

    collect_dict["Items:"] = dict_items
    return collect_dict


def get_result_page_data():
    """final dictionary data list"""
    data_point_list = []
    list_links = get_url()
    for link in list_links:
        driver.get(link)
        general_info()
        get_collection_data()
        print(get_collection_data())
        data_point_list.append(get_collection_data())
        print(data_point_list)
    return data_point_list


if __name__ == '__main__':
    driver.get(START_LINK)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    login()
    go_to_results()
    get_url()
    print(get_result_page_data())


