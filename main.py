from Scrapers import Collections_Scraper, Artists_Scraper, Places_Scraper
from Sothebys_Objects.Sothebys_Objects_with_Id import CollectionWithId, ArtistWithId, CurrencyWithId, PlaceWithId
from Sothebys_Objects.To_SQL_Obj_Visitor import ToSQLObjectVisitor


def test_scrapers():
    # todo test Places_Scraper
    _collections = Collections_Scraper.main()
    # _artists = Artists_Scraper.main()
    _artists = None
    _places = Places_Scraper.main()
    return _collections, _artists, _places


def test_objects_with_ids(_collections, _artists, _places):
    # todo test PlaceWithId
    _collections_with_id = list(map(lambda col, col_id: CollectionWithId(col, col_id),
                                    _collections, range(1, len(_collections) + 1)))
    # _artists_with_ids = list(map(lambda _artist, a_id: ArtistWithId(_artist, a_id), _artists, range(1, len(_artists) + 1)))
    _artists_with_ids = None
    _places_with_ids = list(map(lambda _place, p_id: PlaceWithId(_place, p_id), _places, range(1, len(_places) + 1)))

    for _collection in _collections_with_id:
        print(_collection.unique_id)
        _collection.print_gen_info()
        _collection.print_item_info()
        for _item in _collection.items:
            print(_item.parent_id)
            print(_item.unique_id)

    """
    for _artist in _artists_with_ids:
        print(_artist.unique_id)
        _artist.print()"""
    return _collections_with_id, _artists_with_ids, _places_with_ids


def test_to_sql_objects(_collections_with_id, _artists_with_ids, _places_with_ids):
    to_sql_visitor = ToSQLObjectVisitor
    _collections_to_sql = list(map(lambda col: col.accept(to_sql_visitor), _collections_with_id))
    _items_to_sql = []
    for collection in _collections_with_id:
        _items_to_sql += list(map(lambda item: item.accept(to_sql_visitor), collection.items))
    #_artists_to_sql = list(map(lambda artist: artist.accept(to_sql_visitor), _artists_with_ids))
    _artists_to_sql = None
    _places_to_sql = list(map(lambda place: place.accept(to_sql_visitor), _places_with_ids))
    for collection in _collections_to_sql:
        for column in collection.columns:
            column.print()

    return _collections_to_sql, _items_to_sql, _artists_to_sql, _places_to_sql


collections, artists, places = test_scrapers()
collections_with_id, artists_with_ids, places_with_ids = test_objects_with_ids(collections, artists, places)
collections_to_sql, items_to_sql, artists_to_sql, places_to_sql = test_to_sql_objects(collections_with_id, artists_with_ids, places_with_ids)

collections_to_sql[0].create_table()
items_to_sql[0].create_table()
for collection in collections_to_sql:
    collection.insert_into_table()
for item in items_to_sql:
    item.insert_into_table()


