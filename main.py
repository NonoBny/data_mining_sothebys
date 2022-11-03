import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

# constants
MAKER = '|'

# get the first result page content using requests

page = requests.get("https://www.sothebys.com/en/results?locale=en", headers={"User-Agent": "Mozilla/5.0 (X11; CrOS "
                                                                                            "x86_64 12871.102.0) "
                                                                                            "AppleWebKit/537.36 ("
                                                                                            "KHTML, like Gecko) "
                                                                                            "Chrome/81.0.4044.141 "
                                                                                            "Safari/537.36"},
                    auth=HTTPBasicAuth('noabenayoun1998@gmail.com', 'Wuqu5520'))

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="searchModule")

# for each of the sales displayed on the results page
# data point we are looking for : title of sale, details (date, time and location)
# past or futur auction, currency, items of the sales, estimate price of items, selling price, reserve or no reserve
# description, condition

sothebys_sales = results.find_all("div", class_="Card data-type-auction")
list_sotheby = []

for sothebys_sale in sothebys_sales:
    title_sale = sothebys_sale.find("div", class_="Card-title")
    details_sale = sothebys_sale.find("div", class_="Card-details")

# find the different details of the collection (date, localisation, time)
    if details_sale.text.find(MAKER) == - 1:
        date = details_sale.text
        time = "n/a"
        localisation = "n/a"
    else:
        date = details_sale.text[:details_sale.text.find(MAKER)]
        if details_sale.text.count(MAKER) == 2:
            mk1 = details_sale.text.find(MAKER) + 1
            mk2 = details_sale.text.find(MAKER, mk1)
            time = details_sale.text[mk1:mk2]
            localisation = details_sale.text[mk2 + 1:]
        else:
            time = "n/a"
            localisation = details_sale.text[details_sale.text.find(MAKER) + 1:]

    category_sale = sothebys_sale.find("div", class_="Card-category")
    past_futur = category_sale.text[category_sale.text.find(':')+1:]
    link = sothebys_sale.find("a", class_="Card-info-container")
    link_url = link["href"]
    sotheby_dict = {'Title of sale': title_sale.text.strip(), 'Date': date.strip(),
                    'Time': time.strip(), 'Localisation': localisation.strip(),
                    'Category of sale': past_futur.strip(), "Link": link_url}

# now for each item of each sales the elements


    list_sotheby.append(sotheby_dict)

    print(title_sale.text.strip())
    print(details_sale.text.strip())
    print(category_sale.text.strip(), end="\n" * 2)

print(list_sotheby)

# print(results.prettify())
# print(soup)
