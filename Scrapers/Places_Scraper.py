from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import time
import json
from typing import List
from Sothebys_Objects.Sothebys_Objects import Place

with open('config.json') as config_file:
    data = json.load(config_file)
    places_scraper_data = data["Places_Scraper_Data"]


def get_bio(soup: BeautifulSoup):
    city_bio = soup.find('div', class_='VenueLocationPage-venueDescription')
    if city_bio:
        city_bio = city_bio.text
    else:
        city_bio = soup.find('div', class_="RichTextModule-items").text
    print(city_bio)
    return city_bio


def get_address(soup: BeautifulSoup):
    address = soup.find('div', class_="Address-address")

    if address:
        address = address.text
    else:
        address = 'n/a'
    print(address)
    return address


def get_phone_number(soup: BeautifulSoup):
    phone_number = soup.find('div', class_='Address-phone')
    if phone_number:
        phone_number = phone_number.text
    else:
        phone_number = 'n/a'
    print(phone_number)
    return phone_number


def get_city_info(link: str):
    driver.get(link)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    city_bio = get_bio(soup)
    address = get_address(soup)
    phone_number = get_phone_number(soup)
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
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    main()
