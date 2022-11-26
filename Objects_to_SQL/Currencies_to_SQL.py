from Scrapers import Collections_Scraper
from Objects_to_SQL import Utilility
import time
currency_columns = [Utilility.Column('id', 'int(16)', ['NOT NULL']),
                    Utilility.Column('name', 'varchar(20)', ['COLLATE utf8_bin']),
                    Utilility.Column('dollar_value',  'float(16)', ['COLLATE utf8_bin'])]


def create_currency_table():
    keys = ['PRIMARY KEY (name)']
    Utilility.create_table('currencies', currency_columns, keys)


def insert_into_currency_table(currency):
    arg0 = str(currency.name)
    arg1 = str(currency.dollar_value)
    values = (arg0, arg1)
    column_names = list(map(lambda col: col.name, currency_columns))
    Utilility.insert_into_table('artists', column_names, values)


def load_currency_table(currency):
    map(lambda c: insert_into_currency_table(c), currency)
    return


if __name__ == '__main__':
    # todo implement this better
    data = Collections_Scraper.main()
    with Utilility.connection:
        create_currency_table()
        load_currency_table(data)
