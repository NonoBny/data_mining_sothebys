from Sothebys_Objects.Sothebys_Objects import Artist
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import time
import json
from typing import List

with open('config.json') as config_file:
    data = json.load(config_file)
    artist_scraper_data = data["Artist_Scraper_Data"]

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version='108.0.5359.124').install()), options=options)
print('got here')

def get_artists(soup: BeautifulSoup):
    page_info = soup.find_all("div", class_=artist_scraper_data["page_info"])
    artists = []

    for item_info in page_info:
        if item_info.find("div", class_=artist_scraper_data["item_info_artists"]).text == artist_scraper_data["Artist"]:
            artist_info = item_info.find("h3", class_=artist_scraper_data["artist_info"]).text
            artists.append(Artist(artist_info))

    for artist in artists:
        artist.print()

    return artists


def main() -> List[Artist]:
    url = artist_scraper_data["Starting_Link"]
    driver.get(url)
    time.sleep(data['WAIT_TIME_20'])
    soup = BeautifulSoup(driver.page_source, "html.parser")
    artists = get_artists(soup)

    for i in range(2, 16):
        link = url+'&p='+str(i)
        driver.get(link)
        time.sleep(data['WAIT_TIME_20'])
        soup = BeautifulSoup(driver.page_source, "html.parser")
        artists += get_artists(soup)

    return artists


if __name__ == '__main__':
    main()
