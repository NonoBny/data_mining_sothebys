import pymysql
from pymysql import cursors
from typing import List, Tuple
import datetime
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='collection_db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


class Column:
    def __init__(self, name, data_type: str, options: List[str]):
        self.name = name
        self.data_type = data_type
        self.options = options


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


def create_table(table_name: str, columns: List[Column], keys: List[str]):
    sql = "CREATE TABLE IF NOT EXISTS " + table_name + "(\n"
    for column in columns:
        sql += column.name + ' ' + column.data_type
        for option in column.options:
            sql += ' ' + option
        sql += ','

    sql = sql[:-1]

    for key in keys:
        sql += key + ','
    sql = sql[:-1]

    with connection.cursor() as cursor:
        cursor.execute(sql)
    return


def insert_into_table(table_name: str, columns: List[Column], values: Tuple[str, ...]):
    sql = "INSERT INTO " + table_name + "("
    for column in columns:
        sql += column.name + ',\n'
    sql = sql[:-1] + ")\n"
    sql += "VALUES (" + ("%s,"*len(values))
    sql = sql[:-1] + ")"

    with connection.cursor() as cursor:
        cursor.execute(sql)
    return