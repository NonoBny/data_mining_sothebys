from Scrapers import Collections_Scraper
from Objects_to_SQL import Utilility
place_columns = [Utilility.Column('id', 'int(16)', ['NOT NULL']),
                 Utilility.Column('name', 'varchar(20)', ['COLLATE utf8_bin']),
                 Utilility.Column('country',  'varchar(20)', ['COLLATE utf8_bin']),
                 Utilility.Column('city',  'varchar(20)', ['COLLATE utf8_bin']),
                 Utilility.Column('address',  'varchar(20)', ['COLLATE utf8_bin']),
                 Utilility.Column('phone_number',  'int(16)', ['COLLATE utf8_bin'])]


def create_places_table():
    keys = ['PRIMARY KEY (name)']
    Utilility.create_table('places', place_columns, keys)


def insert_into_places_table(place):
    arg0 = str(place.id)
    arg1 = str(place.name)
    arg2 = str(place.country)
    arg3 = str(place.city)
    arg4 = str(place.address)
    arg5 = str(place.phone_number)
    values = (arg0, arg1, arg2, arg3, arg4, arg5)
    column_names = list(map(lambda col: col.name, place_columns))
    Utilility.insert_into_table('artists', column_names, values)


def load_places_table(place):
    map(lambda c: insert_into_places_table(c), place)
    return


if __name__ == '__main__':
    # todo implement this better
    data = Collections_Scraper.main()
    with Utilility.connection:
        create_places_table()
        load_places_table(data)
