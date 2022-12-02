import pymysql
from pymysql import cursors
from typing import List, Tuple
import json


with open('../config.json.json') as config_file:
    data = json.load(config_file)
    sql_data = data["SQL_DATA"]

connection = pymysql.connect(host=sql_data["HOST"],
                             user=sql_data["USER"],
                             password=sql_data["PASSWORD"],
                             database=sql_data["DATABASE"],
                             charset=sql_data["CHARSET"],
                             cursorclass=pymysql.cursors.DictCursor)


class ForeignKey:
    def __init__(self, table_name: str, table_column_name: str) -> None:
        self.table_name = table_name
        self.table_column_name = table_column_name


class Column:
    def __init__(self, name: str, data_type: str, options: List[str] = None,
                 primary_key: bool = False, foreign_key: ForeignKey = None) -> None:
        if options is None:
            options = []
        self.name = name
        self.data_type = data_type
        self.options = options
        self.primary_key = primary_key

        if foreign_key is None:
            self.foreign_key = False
        else:
            self.foreign_key = foreign_key

    def print(self):
        print(self.name + ' ' + self.data_type + ' ' + str(self.options))


class SothebysSQLObject:
    def __init__(self, table_name: str, columns: List[Column], values: Tuple) -> None:
        self.table_name = table_name
        self.columns = columns
        self.values = values

    def create_table(self) -> None:
        sql = "CREATE TABLE IF NOT EXISTS " + self.table_name + "(\n"
        for column in self.columns:
            sql += column.name + ' ' + column.data_type + ' '

            for option in column.options:
                sql += option + ' '
            sql += ','

        for column in self.columns:
            if column.primary_key:
                sql += f'Primary Key({column.name}),'

        for column in self.columns:
            if column.foreign_key:
                sql += f"FOREIGN KEY ({column.name}) REFERENCES {column.foreign_key.table_name} ({column.foreign_key.table_column_name}),"

        sql = sql[:-1] + ')'

        print(sql)
        with connection.cursor() as cursor:
            cursor.execute(sql)
        return

    def insert_into_table(self) -> None:
        sql = "INSERT INTO " + self.table_name + "("
        for column in self.columns:
            sql += column.name + ','
        sql = sql[:-1] + ") "
        sql += "VALUES (" + ("%s," * len(self.values))
        sql = sql[:-1] + ")"

        print(sql)
        print(self.values)
        with connection.cursor() as cursor:
            cursor.execute(sql, self.values)
        connection.commit()
        return

    def update_row(self) -> None:
        # todo implement this
        pass

    def delete_row(self) -> None:
        # todo implement this
        pass

    def show_table(self) -> None:
        # todo implement this
        pass

    def delete_table(self) -> None:
        # todo implement this
        pass
