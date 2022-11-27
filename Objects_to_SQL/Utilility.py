import pymysql
from pymysql import cursors
from typing import List, Tuple
import datetime
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='sothebys_db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


class Column:
    def __init__(self, name, data_type: str, options=None):
        if options is None:
            options = []
        self.name = name
        self.data_type = data_type
        self.options = options



def date_time_str_to_sql_datetime(collection):
    date_str = collection.date_of_auction
    date_as_date = datetime.datetime.strptime(date_str, '%d %B %Y')
    time_str = collection.time_of_auction
    time_as_time = datetime.datetime.strptime(time_str.split()[0], '%H:%M').time()
    date_of_auction = datetime.datetime.combine(date_as_date, time_as_time)
    return date_of_auction

def create_table(table_name: str, columns: List[Column], keys: List[str]):
    sql = "CREATE TABLE IF NOT EXISTS " + table_name + "(\n"
    for column in columns:
        sql += column.name + ' ' + column.data_type + ' '

        for option in column.options:
            sql += option + ' '
        sql += ','

    for key in keys:
        sql += key + ','
    sql = sql[:-1] + ')'

    print(sql)
    with connection.cursor() as cursor:
        cursor.execute(sql)
    return


def insert_into_table(table_name: str, column_names: List[str], values: Tuple[str, ...]):
    sql = "INSERT INTO " + table_name + "("
    for column_name in column_names:
        sql += column_name + ','
    sql = sql[:-1] + ") "
    sql += "VALUES (" + ("%s,"*len(values))
    sql = sql[:-1] + ")"

    print(sql)
    print(values)
    with connection.cursor() as cursor:
        cursor.execute(sql, values)
    connection.commit()
    return
