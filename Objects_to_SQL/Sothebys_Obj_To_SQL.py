from Objects_to_SQL.Sothebys_SQL_Obj import SothebysSQLObject, Column, ForeignKey
from Sothebys_Objects.Sothebys_Objects_with_Id import CollectionWithId, ItemWithId, ArtPieceWithId, \
    ArtistWithId, CurrencyWithId, PlaceWithId
import datetime
from typing import List, Tuple


artists: List[ArtistWithId] = []
currencies: List[CurrencyWithId] = []
places: List[PlaceWithId] = []


# the lists of all of these objects is needed to get the foreign keys
def set_artist_(_artists: List[ArtistWithId]) -> None:
    global artists
    artists = _artists


def set_currencies(_currencies: List[CurrencyWithId]) -> None:
    global currencies
    currencies = _currencies


def set_places(_places: List[PlaceWithId]) -> None:
    global places
    places = _places


# a function to help get to strings and return a datetime object
def string_to_date_time(collection: CollectionWithId) -> datetime.datetime:
    date_str = collection.date_of_auction
    time_str = collection.time_of_auction
    date_obj = datetime.datetime.strptime(date_str, '%d %B %Y')
    time_obj = datetime.datetime.strptime(time_str.split()[0], '%H:%M').time()
    date_time = datetime.datetime.combine(date_obj, time_obj)
    return date_time


# interface for the following classes
class SothebysObjToSQL:
    def __init__(self, table_name=None, columns=None, values=None) -> None:
        self.table_name = table_name
        self.columns = columns
        self.values = values

    def get_sql_object(self) -> SothebysSQLObject:
        return SothebysSQLObject(self.table_name, self.columns, self.values)

    @staticmethod
    def get_columns() -> List[Column]:
        pass

    @staticmethod
    def get_values(sothebys_obj) -> Tuple:
        pass


# creates an Artist SQL objects
class ArtistToSQL(SothebysObjToSQL):
    def __init__(self, artist: ArtistWithId) -> None:
        super().__init__('artists', self.get_columns(), self.get_values(artist))

    @staticmethod
    def get_columns() -> List[Column]:
        artist_columns = [Column('id', 'int(16)', ['NOT NULL'], primary_key=True),
                          Column('name', 'varchar(255)', ['COLLATE utf8_bin']),
                          Column('life', 'varchar(255)', ['COLLATE utf8_bin']),
                          Column('bio', 'TEXT', ['COLLATE utf8_bin'])]
        return artist_columns

    @staticmethod
    def get_values(artist: ArtistWithId) -> Tuple:
        _id = artist.unique_id
        name = artist.name
        life = artist.life
        bio = artist.bio

        return _id, name, life, bio


# creates a Collection SQL objects
class CollectionToSql(SothebysObjToSQL):
    def __init__(self, collection: CollectionWithId) -> None:
        super().__init__('collections', self.get_columns(), self.get_values(collection))

    @staticmethod
    def get_columns() -> List[Column]:
        collection_columns = [Column('id', 'int(16)', ['NOT NULL'], primary_key=True),
                              Column('title_of_collection', 'varchar(255)', ['COLLATE utf8_bin']),
                              Column('date_of_auction', 'DATETIME'),
                              Column('place_of_auction_id', 'int(16)', ['NOT NULL'],
                                     foreign_key=ForeignKey('places', 'id')),
                              Column('number_of_items', 'int(16)'),
                              Column('type_of_items', 'varchar(255)', ['COLLATE utf8_bin']),
                              Column('total_sale', 'varchar(255)', ['COLLATE utf8_bin'])]
        return collection_columns

    @staticmethod
    def get_values(collection: CollectionWithId) -> Tuple:
        _id = collection.unique_id
        title_of_collection = collection.title_of_collection
        date_of_auction = string_to_date_time(collection)

        place_of_auction = -1
        for place in places:
            if collection.place_of_auction == place.city:
                place_of_auction = place.unique_id

        number_of_items = collection.number_of_items
        type_of_items = collection.type_of_items
        total_sale = collection.total_sale

        return _id, title_of_collection, date_of_auction, place_of_auction, number_of_items, type_of_items, total_sale


# creates a Currency SQL object
class CurrencyToSQL(SothebysObjToSQL):
    def __init__(self, currency: CurrencyWithId) -> None:
        super().__init__('currencies', self.get_columns(), self.get_values(currency))

    @staticmethod
    def get_columns() -> List[Column]:
        currency_columns = [Column('id', 'int(16)', ['NOT NULL'], primary_key=True),
                            Column('name', 'varchar(20)', ['COLLATE utf8_bin']),
                            Column('dollar_value', 'float(16)', ['COLLATE utf8_bin'])]
        return currency_columns

    @staticmethod
    def get_values(currency: CurrencyWithId) -> Tuple:
        _id = currency.unique_id
        name = currency.name
        dollar_value = currency.dollar_value
        return _id, name, dollar_value


# creates an Item SQL object
class ItemToSql(SothebysObjToSQL):
    def __init__(self, item: ItemWithId) -> None:
        super().__init__('items', self.get_columns(), self.get_values(item))

    @staticmethod
    def get_columns() -> List[Column]:

        item_columns = [Column('id', 'int(16)', ['NOT NULL'], primary_key=True),
                        Column('collection_id', 'int(16)', ['NOT NULL'],
                               foreign_key=ForeignKey('collections', 'id')),
                        Column('item_index', 'int(16)', ['NOT NULL']),
                        Column('author_id', 'int(16)', ['NOT NULL'],
                               foreign_key=ForeignKey('artists', 'id')),
                        Column('title', 'varchar(255)', ['COLLATE utf8_bin']),
                        Column('type_of_items', 'varchar(255)', ['COLLATE utf8_bin']),
                        Column('price', 'varchar(255)', ['COLLATE utf8_bin']),
                        Column('currency_id', 'int(16)', ['NOT NULL'],
                               foreign_key=ForeignKey('currencies', 'id')),
                        Column('reserved', 'varchar(255)', ['COLLATE utf8_bin']),
                        Column('estimated_price', 'varchar(255)', ['COLLATE utf8_bin'])]
        return item_columns

    @staticmethod
    def get_values(item: ItemWithId) -> Tuple:
        _id = item.unique_id
        collection_id = item.parent_id
        index = item.index

        author_id = -1
        if type(item) is ArtPieceWithId:
            for author in artists:
                if item.author == author.name:
                    author_id = author.unique_id

        title = item.title
        type_of_items = item.type
        price = item.price_number
        currency_id = -1
        for currency in currencies:
            print('test')
            print(currency.name)
            print(item.price_currency)
            print()
            if item.price_currency == currency.name:
                currency_id = currency.unique_id

        reserved = item.reserve_or_not
        estimated_price = item.estimate_price

        return _id, collection_id, index, author_id, title, type_of_items, price, currency_id, reserved, estimated_price


# creates a place sql object
class PlaceToSQL(SothebysObjToSQL):
    def __init__(self, place: PlaceWithId) -> None:
        super().__init__('places', self.get_columns(), self.get_values(place))

    @staticmethod
    def get_columns() -> List[Column]:
        columns = [Column('id', 'int(16)', ['NOT NULL'], primary_key=True),
                   Column('region_name', 'varchar(255)', ['COLLATE utf8_bin']),
                   Column('city', 'varchar(255)', ['COLLATE utf8_bin']),
                   Column('address', 'varchar(255)', ['COLLATE utf8_bin']),
                   Column('phone_number', 'varchar(255)', ['COLLATE utf8_bin']),
                   Column('bio', 'TEXT', ['COLLATE utf8_bin'])]
        return columns

    @staticmethod
    def get_values(place: PlaceWithId) -> Tuple:
        _id = place.unique_id
        region_name = place.region_name
        city = place.city
        address = place.address
        phone_number = place.phone_number
        bio = place.bio

        return _id, region_name, city, address, phone_number, bio
