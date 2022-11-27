from Sothebys_Objects import Artist
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import json


with open('../config.json') as config_file:
    data = json.load(config_file)

driver = webdriver.Chrome(ChromeDriverManager().install())


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


def main():
    # todo make links and const part of config.json
    # todo implement multi threading with grequests to make this faster
    url = "https://www.sothebys.com/en/search?locale=en&query=artists&tab=artistsmakers"
    driver.get(url)
    time.sleep(data['WAIT_TIME_20'])
    artists = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    artist_links = get_artist_links(soup)

    for i in range(2 ,3):
        link = url+'&p='+str(i)
        driver.get(link)
        time.sleep(data['WAIT_TIME_20'])
        soup = BeautifulSoup(driver.page_source, "html.parser")
        artist_links += get_artist_links(soup)

    print(artist_links)
    for artist_link in artist_links:
        driver.get(artist_link)
        time.sleep(data['WAIT_TIME_20'])
        soup = BeautifulSoup(driver.page_source, "html.parser")
        artists.append(get_artist_data(soup))

    return artists


if __name__ == '__main__':
    main()
