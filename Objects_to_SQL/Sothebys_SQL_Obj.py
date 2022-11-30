import pymysql
from pymysql import cursors


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='sothebys_db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


class ForeignKey:
    def __init__(self, table_name, table_column_name):
        self.table_name = table_name
        self.table_column_name = table_column_name


class Column:
    def __init__(self, name, data_type: str, options=None, primary_key=False, foreign_keys=None):
        if options is None:
            options = []
        self.name = name
        self.data_type = data_type
        self.options = options
        self.primary_key = primary_key

        if foreign_keys is None:
            foreign_keys = []
        self.foreign_key = foreign_keys


class SothebysSQLObject:
    def __init__(self, table_name, columns, values):
        self.table_name = table_name
        self.columns = columns
        self.values = values

    def create_table(self):
        sql = "CREATE TABLE IF NOT EXISTS " + self.table_name + "(\n"
        for column in self.columns:
            sql += column.name + ' ' + column.data_type + ' '

            for option in column.options:
                sql += option + ' '
            sql += ','

        # todo implement keys
        for key in keys:
            sql += key + ','
        sql = sql[:-1] + ')'

        print(sql)
        with connection.cursor() as cursor:
            cursor.execute(sql)
        return

    def insert_into_table(self):
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

    def update_row(self):
        # todo impement this
        pass

    def delete_row(self):
        # todo implement this
        pass

    def show_table(self):
        # todo implement this
        pass

    def delete_table(self):
        # todo implement this
        pass
