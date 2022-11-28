import time

from Scrapers import Collections_Scraper, Artists_Scraper
from Sothebys_Objects import Sothebys_Object_With_Id


collections = Collections_Scraper.main()
time.sleep(100)
artists = Artists_Scraper.main()

collections_with_id = []
c_id = 1
item_id = 1
artist_id = 1
for collection in collections:
    collection_with_id = Sothebys_Object_With_Id.CollectionWithId(collection, c_id)
    items_with_id = []

    for item in collection_with_id.items:
        item_with_id = Sothebys_Object_With_Id.ItemWithId(item, item_id, c_id)
        items_with_id.append(item)
        item_id += 1

    collection_with_id.items = items_with_id
    collections_with_id.append(collection_with_id)
    c_id += 1

for col in collections_with_id:
    print('collection id: ' + str(col._id))
    for item in col.items:
        print('item id: ' + str(item._id))


currencies = []
places = []
for collection in collections:
    places.append(collection.place_of_auction)
    for item in collection.items:
        currencies.append(item.price_currency)

places = list(sorted(list(set(places))))
currencies = list(sorted(list(set(currencies))))
print(places)
print(currencies)

artists_with_ids = []
for artist in artists:
    artist_with_id = Sothebys_Object_With_Id.ArtistWithId(artist, artist_id)
    artists_with_ids.append(artist_with_id)
    artist_id += 1

for artist in artists_with_ids:
    print('artist id: ' + artist._id)

