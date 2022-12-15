import Objects_to_SQL.Sothebys_Obj_To_SQL
from Scrapers import Collections_Scraper, Artists_Scraper, Places_Scraper
from Sothebys_Objects.Sothebys_Objects import Collection, Artist, Currency, Place
from Sothebys_Objects.Sothebys_Objects_with_Id import CollectionWithId, ArtistWithId, CurrencyWithId, PlaceWithId

from Sothebys_Objects.To_SQL_Obj_Visitor import ToSQLObjectVisitor
from typing import List


def get_collections_and_currencies():
    to_sql_visitor = ToSQLObjectVisitor

    collections = Collections_Scraper.main()
    collections_with_id = list(map(lambda col, col_id: CollectionWithId(col, col_id),
                                   collections, range(1, len(collections) + 1)))

    currencies_with_id = get_currencies_with_id(collections_with_id)
    Objects_to_SQL.Sothebys_Obj_To_SQL.set_currencies(currencies_with_id)
    collections_to_sql = list(map(lambda col: col.accept(to_sql_visitor), collections_with_id))
    currencies_to_sql = list(map(lambda currency: currency.accept(to_sql_visitor), currencies_with_id))

    items_to_sql = []
    for _collection in collections_with_id:
        items_to_sql += list(map(lambda item: item.accept(to_sql_visitor), _collection.items))

    currencies_to_sql[0].create_table()
    collections_to_sql[0].create_table()
    items_to_sql[0].create_table()

    list(map(lambda currency: currency.insert_into_table(), currencies_to_sql))
    list(map(lambda collection: collection.insert_into_table(), collections_to_sql))
    list(map(lambda item: item.insert_into_table(), items_to_sql))

    return collections


def get_artists():
    to_sql_visitor = ToSQLObjectVisitor

    artists = Artists_Scraper.main()
    artists_with_ids = list(map(lambda artist, a_id: ArtistWithId(artist, a_id), artists, range(1, len(artists) + 1)))
    artists_with_ids.append(ArtistWithId(Artist(''), -1))
    artists_to_sql = list(map(lambda artist: artist.accept(to_sql_visitor), artists_with_ids))
    artists_to_sql[0].create_table()

    Objects_to_SQL.Sothebys_Obj_To_SQL.set_artist_(artists_with_ids)
    list(map(lambda artist: artist.insert_into_table(), artists_to_sql))
    return artists


def get_places():
    to_sql_visitor = ToSQLObjectVisitor
    places = Places_Scraper.main()
    places_with_ids = list(map(lambda _place, p_id: PlaceWithId(_place, p_id), places, range(1, len(places) + 1)))
    places_with_ids.append(PlaceWithId(Place('', '', '', 0, ''), -1))
    places_to_sql = list(map(lambda place: place.accept(to_sql_visitor), places_with_ids))
    places_to_sql[0].create_table()
    Objects_to_SQL.Sothebys_Obj_To_SQL.set_places(places_with_ids)
    list(map(lambda place: place.insert_into_table(), places_to_sql))
    return places


def get_currencies_with_id(collections_with_id: List[CollectionWithId]) -> List[CurrencyWithId]:
    currency_strs = []
    currencies_with_id = []
    currency_id = 1

    for collection in collections_with_id:
        for item in collection.items:
            if item.price_currency not in currency_strs and item.price_currency != "":
                currency_strs.append(item.price_currency)
                currencies_with_id.append(CurrencyWithId(Currency(item.price_currency), currency_id))
                currency_id += 1

    currencies_with_id.append(CurrencyWithId(Currency(''), -1))
    return currencies_with_id


def main() -> None:
    #get_artists()
    #get_places()
    get_collections_and_currencies()


if __name__ == '__main__':
    main()
