from Objects_to_SQL.Sothebys_SQL_Obj import SothebysSQLObject, Column, ForeignKey
from Sothebys_Objects.Sothebys_Objects_with_Id import CollectionWithId, ItemWithId, ArtPieceWithId, \
    ArtistWithId, CurrencyWithId, PlaceWithId
import datetime
from typing import List, Tuple
import requests
import json
from unidecode import unidecode
import time

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
    def format_name(name):
        words_to_remove = ['sir', 'lord']
        name_substitutions = [('Kazimir', 'Kasimir'), ('Alfonse', 'Alfons'), ('Angelika', 'Angelica')]

        # 'the', 'elder', 'younger',
        print(name)
        name = unidecode(name).lower()
        name = name.replace(' ', '-')
        while name[-1] == '-':
            name = name[:-1]

        while name[0] == '-':
            name = name[1:]

        name = name.split('-and-')[0]
        name = name.split('-')


        clean_word = ''
        for i in range(len(name)):
            if name[i] in words_to_remove or (name[i].count('.') > 1 and i > 0):
                continue
            for j in range(len(name[i])):
                if name[i][j].isalpha() or name[i][j] == '&':
                    clean_word += name[i][j]
            clean_word += ' '

        clean_word = clean_word.replace(' ', '-')

        if clean_word[-1] == '-':
            clean_word = clean_word[:-1]
        clean_word = clean_word.replace('--', '-')
        name = clean_word

        for sub in name_substitutions:
            if sub[0].lower() in name:
                name = name.replace(sub[0].lower(), sub[1].lower())
        if '-the-elder-' in name:
            name = name.replace('-the-elder-', '-')
            name = name + '-the-elder'

        if '-the-younger-' in name:
            name = name.replace('-the-elder-', '-')
            name = name + '-the-elder'
        print(name)
        return name

    @staticmethod
    def get_columns() -> List[Column]:
        artist_columns = [Column('id', 'int(16)', ['NOT NULL'], primary_key=True),
                          Column('name', 'varchar(64)', ['COLLATE utf8_bin']),
                          Column('gender', 'varchar(64)', ['COLLATE utf8_bin']),
                          Column('bio', 'TEXT', ['COLLATE utf8_bin']),
                          Column('birthday', 'varchar(64)', ['COLLATE utf8_bin']),
                          Column('deathday', 'varchar(64)', ['COLLATE utf8_bin']),
                          Column('home_town', 'varchar(64)', ['COLLATE utf8_bin']),
                          Column('location', 'varchar(64)', ['COLLATE utf8_bin'])]
        return artist_columns


    @staticmethod
    def get_data_from_api(artist: ArtistWithId):
        if artist.name == '':
            return
        params = {
            'client_id': '64b2024a34869c2c026e',
            'client_secret': '124aede4d3cf6dfc251bf485ed09f666',
        }
        response = requests.post('https://api.artsy.net/api/tokens/xapp_token', params=params)
        time.sleep(0.2)
        xapp_token = json.loads(response.text)['token']
        print(xapp_token)
        headers = {
            'X-Xapp-Token': xapp_token,
        }

        response = requests.get('https://api.artsy.net/api/artists/'+ArtistToSQL.format_name(artist.name), headers=headers)
        time.sleep(0.2)
        data = json.loads(response.text)
        print(data)
        return data

    @staticmethod
    def get_values(artist: ArtistWithId) -> Tuple:

        _id = artist.unique_id
        name = artist.name

        data = ArtistToSQL.get_data_from_api(artist)
        if data is not None and 'message' not in data.keys():
            gender = data["gender"]
            bio = data["biography"]
            birthday = data["birthday"]
            deathday = data["deathday"]
            hometown = data["hometown"]
            location = data["location"]
        else:
            gender = 'n/a'
            bio = 'n/a'
            birthday = 'n/a'
            deathday = 'n/a'
            hometown = 'n/a'
            location = 'n/a'

        return _id, name, gender, bio, birthday, deathday, hometown, location


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
