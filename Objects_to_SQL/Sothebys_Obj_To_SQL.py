from Objects_to_SQL.Sothebys_SQL_Obj import SotheybysSQLObject, Column, ForeignKey
#from Sothebys_Objects.Sothebys_Objects import SothebysObject
from Sothebys_Objects.Sothebys_Object_With_Id import ArtistWithId, CollectionWithId,\
    ItemWithId, ArtPieceWithId, CurrencyWithId, PlaceWithId

import datetime


# a function to help get to strings and return a datetime object
def string_to_date_time(collection):
    date_str = collection.date_of_auction
    time_str = collection.time_of_auction
    date_obj = datetime.datetime.strptime(date_str, '%d %B %Y')
    time_obj = datetime.datetime.strptime(time_str.split()[0], '%H:%M').time()
    date_time = datetime.datetime.combine(date_obj, time_obj)
    return date_time


# interface for the following classes
class SothebysObjToSQL:
    def __init__(self, table_name=None, columns=None, values=None):
        self.table_name = table_name
        self.columns = columns
        self.values = values

    def get_sql_object(self):
        return SotheybysSQLObject(self.table_name, self.columns, self.values)

    @staticmethod
    def get_columns():
        pass

    @staticmethod
    def get_values(sothebys_obj):
        pass


# creates an Artist SQL objects
class ArtistToSQL(SothebysObjToSQL):
    def __init__(self, artist: ArtistWithId):
        super().__init__('artists', self.get_columns(), self.get_values(artist))

    @staticmethod
    def get_columns():
        artist_columns = [Column('id', 'int(16)', ['NOT NULL'], primary_key=True),
                          Column('name', 'varchar(255)', ['COLLATE utf8_bin']),
                          Column('life', 'varchar(255)', ['COLLATE utf8_bin']),
                          Column('bio', 'TEXT', ['COLLATE utf8_bin'])]
        return artist_columns

    @staticmethod
    def get_values(artist: ArtistWithId):
        _id = artist._id
        name = artist.name
        life = artist.life
        bio = artist.bio

        return _id, name, life, bio


# creates a Collection SQL objects
class CollectionToSql(SothebysObjToSQL):
    def __init__(self, collection: CollectionWithId):
        super().__init__('collections', self.get_columns(), self.get_values(collection))

    @staticmethod
    def get_columns():
        collection_columns = [Column('id', 'int(16)', ['NOT NULL'], primary_key=True),
                              Column('title_of_collection', 'varchar(255)', ['COLLATE utf8_bin']),
                              Column('date_of_auction', 'DATETIME'),
                              Column('place_of_auction', 'varchar(255)', ['COLLATE utf8_bin']),
                              Column('number_of_items', 'int(16)'),
                              Column('type_of_items', 'varchar(255)', ['COLLATE utf8_bin']),
                              Column('total_sale', 'varchar(255)', ['COLLATE utf8_bin'])]
        return collection_columns

    @staticmethod
    def get_values(collection: CollectionWithId):
        _id = collection._id
        title_of_collection = collection.title_of_collection
        date_of_auction = string_to_date_time(collection)
        place_of_auction = collection.place_of_auction
        number_of_items = collection.number_of_items
        type_of_items = collection.type_of_items
        total_sale = collection.total_sale

        return _id, title_of_collection, date_of_auction, place_of_auction, number_of_items, type_of_items, total_sale


# creates a Currency SQL object
class CurrencyToSQL(SothebysObjToSQL):
    def __init__(self, currency: CurrencyWithId):
        super().__init__('currencies', self.get_columns(), self.get_values(currency))

    @staticmethod
    def get_columns():
        currency_columns = [Column('id', 'int(16)', ['NOT NULL'], primary_key=True),
                            Column('name', 'varchar(20)', ['COLLATE utf8_bin']),
                            Column('dollar_value', 'float(16)', ['COLLATE utf8_bin'])]
        return currency_columns

    @staticmethod
    def get_values(currency: CurrencyWithId):
        _id = currency._id
        pass


# creates an Item SQL object
class ItemToSql(SothebysObjToSQL):
    def __init__(self, item: ItemWithId):
        super().__init__('items', self.get_columns(), self.get_values(item))

    @staticmethod
    def get_columns():

        item_columns = [Column('id', 'int(16)', ['NOT NULL'], primary_key=True),
                        Column('collection_id', 'int(16)', ['NOT NULL'],
                               foreign_keys=[ForeignKey('collections', 'id')]),
                        Column('index', 'int(16)', ['NOT NULL']),
                        Column('author', 'varchar(255)', ['COLLATE utf8_bin']),
                        Column('title', 'varchar(255)', ['COLLATE utf8_bin']),
                        Column('type_of_items', 'varchar(255)', ['COLLATE utf8_bin']),
                        Column('price', 'float(16)'),
                        Column('currency', 'varchar(255)', ['COLLATE utf8_bin']),
                        Column('reserved', 'varchar(255)', ['COLLATE utf8_bin']),
                        Column('estimated_price', 'varchar(255)', ['COLLATE utf8_bin'])]
        return item_columns

    @staticmethod
    def get_values(item: ItemWithId):
        _id = item._id
        collection_id = item.collection_id # todo implement this
        index = item.index
        if type(item) is ArtPieceWithId:
            author = item.author
        else:
            author = 'n/a'

        title = item.title
        type_of_items = str(type(item))
        price = item.price_number
        currency = item.price_currency
        reserved = item.reserve_or_not
        estimated_price = item.estimate_price

        return _id, collection_id, index, author, title, type_of_items, price, currency, reserved, estimated_price


# creates a place sql object
class PlaceToSQL:
    def __init__(self, place: PlaceWithId):
        self.table_name = 'places'
        self.columns = self.get_columns()
        self.values = self.get_values(place)

    @staticmethod
    def get_columns():
        # todo impement this
        pass

    @staticmethod
    def get_values(place: PlaceWithId):
        # todo impement this
        pass
