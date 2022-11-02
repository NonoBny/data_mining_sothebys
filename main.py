import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup


page = requests.get("https://www.sothebys.com/en/results?locale=en", headers={"User-Agent": "Mozilla/5.0 (X11; CrOS "
                                                                                            "x86_64 12871.102.0) "
                                                                                            "AppleWebKit/537.36 ("
                                                                                            "KHTML, like Gecko) "
                                                                                            "Chrome/81.0.4044.141 "
                                                                                            "Safari/537.36"},
                    auth=HTTPBasicAuth('noabenayoun1998@gmail.com', 'Wuqu5520'))


soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="searchModule")

sothebys_sales = results.find_all("div", class_="Card data-type-auction")
for sothebys_sale in sothebys_sales:
    title_sale = sothebys_sale.find("div", class_="Card-title")
    details_sale = sothebys_sale.find("div", class_="Card-details")
    category_sale = sothebys_sale.find("div", class_="Card-category")
    print(title_sale.text)
    print(details_sale.text)
    print(category_sale.text, end="\n"*2)

#print(results.prettify())
#print(soup)

