from Objects.Artist import Artist
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


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
    for i in range(14, 16):
        print(i)
    print("test")
    url = "https://www.sothebys.com/en/search?locale=en&query=artists&tab=artistsmakers"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    artist_links = get_artist_links(soup)
    artists = []
    for i in range(15, 16):
        print()
        driver.get(url+'&p='+str(i))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        artist_links += get_artist_links(soup)

    for artist_link in artist_links:
        driver.get(artist_link)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        artists.append(get_artist_data(soup))

    return artists


if __name__ == '__main__':
    main()
