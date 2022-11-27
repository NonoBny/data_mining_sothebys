
import copy

from Scrapers import Collections_Scraper
from Objects_to_SQL import Utilility
import Sothebys_Objects
import datetime

collection_id = 1
item_id = 1
collection_columns = [Utilility.Column('id', 'int(16)', ['NOT NULL']),
                      Utilility.Column('title_of_collection', 'varchar(255)', ['COLLATE utf8_bin']),
                      Utilility.Column('date_of_auction', 'DATETIME'),
                      Utilility.Column('place_of_auction', 'varchar(255)', ['COLLATE utf8_bin']),
                      Utilility.Column('number_of_items', 'int(16)'),
                      Utilility.Column('type_of_items', 'varchar(255)', ['COLLATE utf8_bin']),
                      Utilility.Column('total_sale', 'varchar(255)', ['COLLATE utf8_bin'])]

item_columns = [Utilility.Column('id', 'int(16)', ['NOT NULL']),
                Utilility.Column('collection_id', 'int(16)', ['NOT NULL']),
                Utilility.Column('item_no', 'int(16)', ['NOT NULL']),
                Utilility.Column('author', 'varchar(255)', ['COLLATE utf8_bin']),
                Utilility.Column('title', 'TEXT', ['COLLATE utf8_bin']),
                Utilility.Column('type_of_item', 'varchar(255)', ['COLLATE utf8_bin']),
                Utilility.Column('price', 'int(16)', ['COLLATE utf8_bin']),
                Utilility.Column('currency', 'varchar(3)'),
                Utilility.Column('estimated_price', 'varchar(255)')]


def string_to_date_time(collection):
    date_str = collection.date_of_auction
    time_str = collection.time_of_auction
    date_obj = datetime.datetime.strptime(date_str, '%d %B %Y')
    time_obj = datetime.datetime.strptime(time_str.split()[0], '%H:%M').time()
    date_time = datetime.datetime.combine(date_obj, time_obj)
    return date_time


def create_collection_table():
    keys = ['PRIMARY KEY (id)']
    Utilility.create_table('collections', collection_columns, keys)


def create_items_table():
    keys = ['PRIMARY KEY (id)', 'FOREIGN KEY (collection_id) REFERENCES collections(id)']
    Utilility.create_table('items', item_columns, keys)


def insert_into_collections_table(collection):
    global collection_id
    arg0 = str(collection_id)
    arg1 = str(collection.title_of_collection)
    arg2 = string_to_date_time(collection)
    arg3 = str(collection.place_of_auction)
    arg4 = str(collection.number_of_items)
    arg5 = str(collection.type_of_items)
    arg6 = str(collection.total_sale)
    values = (arg0, arg1, arg2, arg3, arg4, arg5, arg6)
    column_names = list(map(lambda col: col.name, collection_columns))
    print('testing column names')
    print(column_names)
    Utilility.insert_into_table('collections', column_names, values)
    load_items_table(collection.items, collection_id)
    collection_id += 1


def load_collection_table(collections):
    print('testing load_collection_table')
    list(map(lambda c: insert_into_collections_table(c), collections))
    return


def insert_into_items_table(item, collection_id):
    print('testing insert_into_items_table')
    global item_id
    arg_id = str(copy.copy(item_id))
    item_id += 1

    arg0 = str(collection_id)
    arg1 = str(item.index)
    if type(item) is Sothebys_Objects.ArtPiece:
        arg2 = str(item.author)
    else:
        arg2 = 'n/a'
    arg3 = str(item.title)[0:min(len(item.title), 255)]
    arg4 = str(item.type)
    arg5 = str(item.price_number).replace(',', '')
    if arg5 == 'not sold':
        arg5 = str(-1)
    arg6 = str(item.price_currency)
    arg7 = str(item.estimate_price)
    values = (arg_id, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)
    item_names = list(map(lambda col: col.name, item_columns))
    Utilility.insert_into_table('items', item_names, values)


def load_items_table(items, collection_id):
    print('testing load_items_table')
    list(map(lambda item: insert_into_items_table(item, collection_id), items))


if __name__ == '__main__':
    # todo try to make this more generic need a function that turns any object into an sql query
    #  probably a decorator or visitor design pattern
    data = Collections_Scraper.main()
    with Utilility.connection:
        create_collection_table()
        create_items_table()
        load_collection_table(data)
