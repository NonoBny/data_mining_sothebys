from Scrapers import Collections_Scraper, Artists_Scraper, Places_Scraper
from Sothebys_Objects.Sothebys_Objects_with_Id import CollectionWithId, ArtistWithId, CurrencyWithId, PlaceWithId


collections = Collections_Scraper.main()
artists = Artists_Scraper.main()
places = Places_Scraper.main()

collections_with_id = list(map(lambda col, col_id: CollectionWithId(col, col_id),
                               collections, range(1, len(collections)+1)))
artists_with_ids = list(map(lambda artist, a_id: ArtistWithId(artist, a_id), artists, range(1, len(artists)+1)))
places_with_ids = list(map(lambda place, p_id: ArtistWithId(place, p_id), places, range(1, len(places)+1)))

currencies = []
for collection in collections:
    for item in collection.items:
        currencies.append(item.price_currency)
currencies = list(sorted(list(set(currencies))))

for collection in collections_with_id:
    print(collection.unique_id)
    collection.print_gen_info()
    collection.print_item_info()
    for item in collection.items:
        print(item.parent_id)
        print(item.unique_id)

for artist in artists_with_ids:
    print(artist.unique_id)
    artist.print()

currencies.remove('')
print(currencies)

