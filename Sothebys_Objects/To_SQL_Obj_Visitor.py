# from Sothebys_Objects.Sothebys_Objects import SothebysObject, Artist, Collection, Item, ArtPiece, Currency, Place
from Objects_to_SQL.Sothebys_Obj_To_SQL import SothebysObjToSQL, ArtistToSQL, \
    CollectionToSql, ItemToSql, CurrencyToSQL, PlaceToSQL
from Sothebys_Objects.Visitor import Visitor

# todo figure out if I should use objWithId or obj


class ToSQLObjectVisitor(Visitor):
    @staticmethod
    def visit_sothebys_object(sothebys_object):
        return SothebysObjToSQL(sothebys_object).get_sql_object()

    @staticmethod
    def visit_artist(artist):
        return ArtistToSQL(artist).get_sql_object()

    @staticmethod
    def visit_collection(collection):
        return CollectionToSql(collection).get_sql_object()

    @staticmethod
    def visit_item(item):
        return ItemToSql(item).get_sql_object()

    @staticmethod
    def visit_art_piece(art_piece):
        return ItemToSql(art_piece).get_sql_object()

    @staticmethod
    def visit_currency(currency):
        return CurrencyToSQL(currency).get_sql_object()

    @staticmethod
    def visit_place(place):
        return PlaceToSQL(place).get_sql_object()
