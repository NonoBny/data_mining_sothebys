from Sothebys_Objects.Sothebys_Objects import Artist
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import json
from typing import List

with open('config.json') as config_file:
    data = json.load(config_file)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def get_artist_short(soup: BeautifulSoup):
    page_info = soup.find_all("div", class_="_1NKmJc-dm-eCxS4OCrXrR5")
    artists = []

    for item_info in page_info:
        if item_info.find("div", class_="_3NZctpq_uZ_mC8NSFPQqk_").text == "Artist":
            artist_info = item_info.find("h3", class_="_3Dm_PuL3C5IuyJed8hRgRn").text
            artists.append(Artist(artist_info, '', ''))

    for artist in artists:
        artist.print()

    return artists


def get_artist_links(soup: BeautifulSoup):
    page_info = soup.find_all("div", class_="_1NKmJc-dm-eCxS4OCrXrR5")
    artists_info = []

    for item_info in page_info:
        if item_info.find("div", class_="_3NZctpq_uZ_mC8NSFPQqk_").text == "Artist":
            artist_info = item_info.find("div", class_="_3AU1X3oKP8TOvGyzhJI6eh oK8AyI4p9HdIRc7HuYLz6")
            artists_info.append(artist_info)

    artist_links = list(map(lambda a: a.find("a").get("href"), artists_info))
    print(artist_links)
    return artist_links


def get_artist_data(soup: BeautifulSoup):
    name = soup.find("h1", class_="ArtistPage-pageHeading").text
    life = soup.find("div", class_="ArtistPage-artistInfo")
    if life is not None:
        life = life.text
    else:
        life = 'currently alive'
    bio = soup.find("div", class_="ArtistPage-bioText").text

    print(name)
    print(life)
    print(bio)

    artist = Artist(name, life, bio)
    return artist


def main() -> List[Artist]:
    # todo make links and const part of config.json
    # todo implement multi threading with grequests to make this faster
    url = "https://www.sothebys.com/en/search?locale=en&query=artists&tab=artistsmakers"
    driver.get(url)
    time.sleep(data['WAIT_TIME_20'])
    soup = BeautifulSoup(driver.page_source, "html.parser")
    artists = get_artist_short(soup)

    for i in range(2, 16):
        link = url+'&p='+str(i)
        driver.get(link)
        time.sleep(data['WAIT_TIME_20'])
        soup = BeautifulSoup(driver.page_source, "html.parser")
        artists += get_artist_short(soup)

    return artists


if __name__ == '__main__':
    main()
