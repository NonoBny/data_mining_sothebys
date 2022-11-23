import pymysql
from pymysql import cursors

import Collection
import webscraper
import datetime

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='collection_db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def create_collection_table():
    sql = """CREATE TABLE IF NOT EXISTS collections (
          id int(11) NOT NULL,
          title_of_collection varchar(255) COLLATE utf8_bin,
          date_of_auction DATETIME,
          place_of_auction varchar(255) COLLATE utf8_bin,
          number_of_items int(11),
          type_of_items varchar(255) COLLATE utf8_bin,
          total_sale varchar(255) COLLATE utf8_bin,
          PRIMARY KEY (id)
          )"""

    with connection.cursor() as cursor:
        cursor.execute(sql)
    return


def create_items_table():
    sql = """CREATE TABLE IF NOT EXISTS items (
          collection_id int(11) NOT NULL,
          item_no int(11) NOT NULL,
          author varchar(255) COLLATE utf8_bin,
          title varchar(65535) COLLATE utf8_bin,
          type_of_item varchar(255) COLLATE utf8_bin,
          price int(11),
          currency varchar(3),
          estimated_price varchar(255),
          FOREIGN KEY (collection_id) REFERENCES collections(id)
          )"""

    with connection.cursor() as cursor:
        cursor.execute(sql)
    return


def get_date_time(date_str, time_str):
    date = date_str.split()
    time = time_str.split()

    year = int(date[2])
    month = int(datetime.datetime.strptime(date[1], '%B').month)
    day = int(date[0])

    hours_min = time[0].split(':')
    hours = int(hours_min[0])
    minutes = int(hours_min[1])
    # timezone = time[1]
    _date = datetime.datetime(year=year, month=month, day=day)

    return _date


def load_collection_table():
    sql = """INSERT INTO collections (id, title_of_collection, date_of_auction, 
    place_of_auction, number_of_items, type_of_items, total_sale)
    VALUES (%s, %s, %s, %s, %s, %s, %s) 
    """

    collection_id = 1
    for collection in data:
        arg0 = str(collection_id)
        arg1 = str(collection.title_of_collection)
        arg2 = str(get_date_time(collection.date_of_auction, collection.time_of_auction))
        arg3 = str(collection.place_of_auction)
        arg4 = str(collection.number_of_items)
        arg5 = str(collection.type_of_Items)
        arg6 = str(collection.total_sale)
        args = (arg0, arg1, arg2, arg3, arg4, arg5, arg6)
        with connection.cursor() as cursor:
            cursor.execute(sql, args)
        load_items_table(collection.items, collection_id)
        collection_id += 1

    return


def load_items_table(items, collection_id):
    sql = """INSERT INTO items (collection_id, item_no, author, title, type_of_item, price, currency, estimated_price)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
    """
    for item in items:
        arg0 = str(collection_id)
        arg1 = str(item.index)
        if type(item) is Collection.ArtPiece:
            arg2 = str(item.author)
        else:
            arg2 = ''
        arg3 = str(item.title)[0:min(len(item.title), 255)]
        arg4 = str(item.type)
        arg5 = str(item.price_number).replace(',', '')
        if arg5 == 'not sold':
            arg5 = str(-1)
        arg6 = str(item.price_currency)
        arg7 = str(item.estimate_price)
        args = (arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

        with connection.cursor() as cursor:
            cursor.execute(sql, args)

    return


if __name__ == '__main__':
    data = webscraper.main()
    with connection:
        create_collection_table()
        create_items_table()
        load_collection_table()
