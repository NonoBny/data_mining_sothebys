from Objects import Collection
from Scrapers import Collections_Scraper
from Objects_to_SQL import Utilility

collection_columns = [Utilility.Column('id', 'int(16)', ['NOT NULL']),
                      Utilility.Column('title_of_collection', 'varchar(255)', ['COLLATE utf8_bin']),
                      Utilility.Column('date_of_auction', 'DATETIME'),
                      Utilility.Column('place_of_auction', 'varchar(255)', ['COLLATE utf8_bin']),
                      Utilility.Column('number_of_items', 'int(16)'),
                      Utilility.Column('type_of_items', 'varchar(255)', ['COLLATE utf8_bin']),
                      Utilility.Column('total_sale', 'varchar(255)', ['COLLATE utf8_bin'])]

item_columns = [Utilility.Column('collection_id', 'int(16)', ['NOT NULL']),
                Utilility.Column('id', 'int(16)', ['NOT NULL']),
                Utilility.Column('item_no', 'int(16)', ['NOT NULL']),
                Utilility.Column('author', 'varchar(255)', ['COLLATE utf8_bin']),
                Utilility.Column('title', 'TEXT', ['COLLATE utf8_bin']),
                Utilility.Column('type_of_item', 'varchar(255)', ['COLLATE utf8_bin']),
                Utilility.Column('price', 'int(16)', ['COLLATE utf8_bin']),
                Utilility.Column('currency', 'varchar(3)'),
                Utilility.Column('estimated_price', 'varchar(255)')]


def create_collection_table():
    keys = ['PRIMARY KEY (id)']
    Utilility.create_table('collections', collection_columns, keys)


def create_items_table():
    keys = ['FOREIGN KEY (collection_id) REFERENCES collections(id)']
    Utilility.create_table('items', item_columns, keys)


def insert_into_collections_table(collection, collection_id):
    arg0 = str(collection_id)
    arg1 = str(collection.title_of_collection)
    arg2 = str(Utilility.get_date_time(collection.date_of_auction, collection.time_of_auction))
    arg3 = str(collection.place_of_auction)
    arg4 = str(collection.number_of_items)
    arg5 = str(collection.type_of_Items)
    arg6 = str(collection.total_sale)
    values = (arg0, arg1, arg2, arg3, arg4, arg5, arg6)
    column_names = list(map(lambda col: col.name, collection_columns))
    print('testing column names')
    print(column_names)
    Utilility.insert_into_table('collections', column_names, values)
    load_items_table(collection.items, collection_id)


def load_collection_table(collections):
    print('testing load_collection_table')
    list(map(lambda c, c_id: insert_into_collections_table(c, c_id), collections, range(len(collections))))
    return


def insert_into_items_table(item, collection_id):
    print('testing insert_into_items_table')
    arg0 = str(collection_id)
    arg1 = str(item.index)
    if type(item) is Collection.ArtPiece:
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
    values = (arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)
    item_names = list(map(lambda col: col.name, item_columns))
    Utilility.insert_into_table('items', item_names, values)


def load_items_table(items, collection_id):
    print('testing load_items_table')
    list(map(lambda item: insert_into_items_table(item, collection_id), items))


if __name__ == '__main__':
    data = webscraper.main()
    with Utilility.connection:
        create_collection_table()
        create_items_table()
        load_collection_table(data)
