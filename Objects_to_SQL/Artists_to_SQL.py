from Scrapers import Artists_Scraper
from Objects_to_SQL import Utilility
artist_columns = [Utilility.Column('name', 'varchar(20)', ['COLLATE utf8_bin']),
                  Utilility.Column('bio',  'varchar(20)', ['COLLATE utf8_bin'])]


def create_artist_table():
    keys = ['PRIMARY KEY (name)']
    Utilility.create_table('artists', artist_columns, keys)


def insert_into_artists_table(artist):
    arg0 = str(artist.name)
    arg1 = str(artist.bio)
    values = (arg0, arg1)
    column_names = list(map(lambda col: col.name, artist_columns))
    Utilility.insert_into_table('artists', column_names, values)


def load_artist_table(artists):
    map(lambda c_id, c: insert_into_artists_table(c), artists)
    return


if __name__ == '__main__':
    data = Artists_Scraper.main()
    with Utilility.connection:
        create_artist_table()
        load_artist_table(data)
