import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup


page = requests.get("https://www.sothebys.com/en/results?locale=en", headers={"User-Agent": "Mozilla/5.0 (X11; CrOS "
                                                                                            "x86_64 12871.102.0) "
                                                                                            "AppleWebKit/537.36 ("
                                                                                            "KHTML, like Gecko) "
                                                                                            "Chrome/81.0.4044.141 "
                                                                                            "Safari/537.36"})

#variables

list_items = []

def separate_coll_details(string_det):
    list_detail = string_det.split("|")
    if string_det.count("|") == 2:
        date_sale = list_detail[0].strip()
        time_sale = list_detail[1].strip()
        place_sale = list_detail[2].strip()
    elif string_det.count("|") == 1:
        date_sale = list_detail[0].strip()
        time_sale = "n/a"
        place_sale = list_detail[1].strip()
    else:
        date_sale = list_detail[0].strip()
        time_sale = "n/a"
        place_sale = "n/a"
    return date_sale, time_sale, place_sale


def general_info(list_card_page):
    for sothebys_sale in list_card_page:
        title_sale = sothebys_sale.find("div", class_="Card-title")
        details_sale = sothebys_sale.find("div", class_="Card-details")
        category_sale = sothebys_sale.find("div", class_="Card-category")
        if category_sale.text == "Category: Past Auction":
            index_car = category_sale.text.find(":")
            category_sale_str = category_sale.text[index_car+1:].strip()
            each_collection_general_det = {"Title of Collection": title_sale.text, "Date of Sale": separate_coll_details(details_sale.text)[0], "Time of Sale": separate_coll_details(details_sale.text)[1], "Place of Sale": separate_coll_details(details_sale.text)[2], "Category": category_sale_str}
            print(each_collection_general_det)
            list_items.append(each_collection_general_det)


if __name__ == '__main__':
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="searchModule")
    sothebys_sales = results.find_all("div", class_="Card data-type-auction")
    general_info(sothebys_sales)
    print(list_items)

