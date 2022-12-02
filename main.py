import Objects_to_SQL.Sothebys_Obj_To_SQL
from Scrapers import Collections_Scraper, Artists_Scraper, Places_Scraper
from Sothebys_Objects.Sothebys_Objects import Collection, Artist, Currency, Place
from Sothebys_Objects.Sothebys_Objects_with_Id import CollectionWithId, ArtistWithId, CurrencyWithId, PlaceWithId
from Objects_to_SQL.Sothebys_Obj_To_SQL import CollectionToSql, ItemToSql, ArtistToSQL, CurrencyToSQL, PlaceToSQL
from Sothebys_Objects.To_SQL_Obj_Visitor import ToSQLObjectVisitor
from typing import List, Tuple


def scrape_objects() -> Tuple[List[Collection], List[Artist], List[Place]]:
    """
    will scrap the website for these types of items
    :return: the 3 lists of scraped items
    """
    # todo test Places_Scraper
    collections = Collections_Scraper.main()

    artists = Artists_Scraper.main()

    places = Places_Scraper.main()

    return collections, artists, places


def get_currencies_with_id(collections_with_id: List[CollectionWithId]) -> List[CurrencyWithId]:
    currency_strs = []
    currencies_with_id = []
    currency_id = 1

    for collection in collections_with_id:
        for item in collection.items:
            if item.price_currency not in currency_strs:
                currency_strs.append(item.price_currency)
                currencies_with_id.append(CurrencyWithId(Currency(item.price_currency), currency_id))
                currency_id += 1
    return currencies_with_id


def get_objects_with_ids(collections: List[Collection], artists: List[Artist], places: List[Place]) \
        -> Tuple[List[CollectionWithId], List[ArtistWithId], List[CurrencyWithId], List[PlaceWithId]]:

    # todo test PlaceWithId
    collections_with_id = list(map(lambda col, col_id: CollectionWithId(col, col_id),
                                   collections, range(1, len(collections) + 1)))

    artists_with_ids = list(map(lambda _artist, a_id: ArtistWithId(_artist, a_id), artists, range(1, len(artists) + 1)))

    _places_with_ids = list(map(lambda _place, p_id: PlaceWithId(_place, p_id), places, range(1, len(places) + 1)))

    currencies_with_id = get_currencies_with_id(collections_with_id)

    return collections_with_id, artists_with_ids, currencies_with_id, _places_with_ids


def get_to_sql_objects(collections_with_id: List[CollectionWithId], artists_with_ids: List[ArtistWithId],
                       currencies_with_id: List[CurrencyWithId], places_with_ids: List[PlaceWithId]) \
        -> Tuple[List[CollectionToSql], List[ItemToSql], List[ArtistToSQL], List[CurrencyToSQL], List[PlaceToSQL]]:

    to_sql_visitor = ToSQLObjectVisitor

    collections_to_sql = list(map(lambda col: col.accept(to_sql_visitor), collections_with_id))

    items_to_sql = []
    for collection in collections_with_id:
        items_to_sql += list(map(lambda item: item.accept(to_sql_visitor), collection.items))

    artists_to_sql = list(map(lambda artist: artist.accept(to_sql_visitor), artists_with_ids))

    places_to_sql = list(map(lambda place: place.accept(to_sql_visitor), places_with_ids))

    currencies_to_sql = list(map(lambda currency: currency.accept(to_sql_visitor), currencies_with_id))

    return collections_to_sql, items_to_sql, artists_to_sql, currencies_to_sql, places_to_sql


def create_tables(collections_to_sql, items_to_sql, artists_to_sql, currencies_to_sql, places_to_sql) -> None:
    collections_to_sql[0].create_table()

    items_to_sql[0].create_table()

    artists_to_sql[0].create_table()

    currencies_to_sql[0].create_table()

    places_to_sql[0].create_table()


def load_tables(collections_to_sql: List[CollectionToSql], items_to_sql: List[ItemToSql],
                artists_to_sql: List[ArtistToSQL], currencies_to_sql: List[CurrencyToSQL],
                places_to_sql: List[PlaceToSQL]) -> None:

    list(map(lambda collection: collection.insert_into_table(), collections_to_sql))

    list(map(lambda item: item.insert_into_table(), items_to_sql))

    list(map(lambda artist: artist.insert_into_table(), artists_to_sql))

    list(map(lambda currency: currency.insert_into_table(), currencies_to_sql))

    list(map(lambda place: place.insert_into_table(), places_to_sql))


def main() -> None:
    collections, artists, places = scrape_objects()

    collections_with_id, artists_with_ids, currencies_with_id, places_with_ids \
        = get_objects_with_ids(collections, artists, places)

    Objects_to_SQL.Sothebys_Obj_To_SQL.set_global_variables(artists_with_ids, currencies_with_id, places_with_ids)

    collections_to_sql, items_to_sql, artists_to_sql, currencies_to_sql, places_to_sql \
        = get_to_sql_objects(collections_with_id, artists_with_ids, currencies_with_id, places_with_ids)

    create_tables(collections_to_sql, items_to_sql, artists_to_sql, currencies_to_sql, places_to_sql)

    load_tables(collections_to_sql, items_to_sql, artists_to_sql, currencies_to_sql, places_to_sql)


if __name__ == '__main__':
    main()
