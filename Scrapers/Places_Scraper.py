from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import json
from typing import List
from Sothebys_Objects.Sothebys_Objects import Place

with open('config.json') as config_file:
    data = json.load(config_file)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def get_city_info(link: str):
    driver.get(link)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    city_bio = soup.find('div', class_='VenueLocationPage-venueDescription')

    if city_bio:
        city_bio = city_bio.text
    else:
        city_bio = soup.find('div', class_="RichTextModule-items").text
    print(city_bio)

    address = soup.find('div', class_="Address-address")

    if address:
        address = address.text
    else:
        address = 'n/a'

    phone_number = soup.find('div', class_='Address-phone')
    if phone_number:
        phone_number = phone_number.text
    else:
        phone_number = 'n/a'

    print(address)
    print(phone_number)
    return address, phone_number, city_bio


def get_cities_in_region(cities, region_name):
    places: List[Place] = list()
    for city in cities:
        city_info = city.find('div', 'PromoLink-title').find('a')
        city_name = city_info.text
        city_page_link = city_info.get('href')
        print('\tCity: ' + city_name + ' ' + city_page_link)
        address, phone_number, bio = get_city_info(city_page_link)
        place = Place(region_name, city_name, address, phone_number, bio)
        places.append(place)
    return places


def get_regions(soup: BeautifulSoup):
    places: List[Place] = list()
    regions = soup.find_all('li', class_='TextOnlyList-items-item')
    for region in regions:
        region_name = region.find('div', class_='TextOnlyListNonCollapsible-title').text
        cities = region.find_all('li', class_='TextOnlyListNonCollapsible-items-item')
        print('Region: ' + region_name)
        places += get_cities_in_region(cities, region_name)
    return places


def main() -> List[Place]:
    driver.get('https://www.sothebys.com/en/about/locations?locale=en')
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    locations = soup.find('div', class_="UnevenTwoColumnContainer-columnOne")
    return get_regions(locations)


if __name__ == '__main__':
    main()

