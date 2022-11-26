from Scrapers import Artists_Scraper
from Objects_to_SQL import Utilility
import time
artist_columns = [Utilility.Column('id', 'int(16)', ['NOT NULL']),
                  Utilility.Column('name', 'varchar(255)', ['COLLATE utf8_bin']),
                  Utilility.Column('life', 'varchar(255)', ['COLLATE utf8_bin']),
                  Utilility.Column('bio',  'TEXT', ['COLLATE utf8_bin'])]


def create_artist_table():
    keys = ['PRIMARY KEY (id)']
    Utilility.create_table('artists', artist_columns, keys)


def insert_into_artists_table(artist, artist_id):
    arg0 = str(artist_id)
    arg1 = str(artist.name)
    arg2 = str(artist.life)
    arg3 = str(artist.bio)
    values = (arg0, arg1, arg2, arg3)
    column_names = list(map(lambda col: col.name, artist_columns))
    Utilility.insert_into_table('artists', column_names, values)


def load_artist_table(artists):
    list(map(lambda artist, artist_id: insert_into_artists_table(artist, artist_id), artists, range(len(artists))))
    return


if __name__ == '__main__':
    # todo try to make this more generic need a function that turns any object into an sql query
    data = Artists_Scraper.main()
    with Utilility.connection:
        create_artist_table()
        load_artist_table(data)
