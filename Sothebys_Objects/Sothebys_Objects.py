from Sothebys_Objects.Visitor import Visitor
from currency_converter import CurrencyConverter


class SothebysObject:
    def print(self):
        pass

    def accept(self, visitor: Visitor):
        return visitor.visit_sothebys_object(self)


class Artist(SothebysObject):
    """
    A simple class of an artist on the Sotheybs website
    """
    def __init__(self, name: str, life: str, bio: str):
        """
        :param name: the name of the artist
        :param life: the birth and death year of an artist (if no longer alive)
        :param bio: a short story of the artist
        """
        self.name = name
        self.life = life
        self.bio = bio

    def print(self):
        """
        will print the Artist in a nice way
        :return: none
        """
        print(f'Artist Name: {str(self.name)}\n+Life: {str(self.life)}\n+ Biography {str(self.bio)}')

    def accept(self, visitor: Visitor):
        return visitor.visit_artist(self)


class Collection(SothebysObject):
    """
       This Class will contain sotheybs collection data
       A collection is a list of items all sold as a single collection
       It contains the collection specific info as well as a list of item objects
       """
    def __init__(self, gen_info, number_items, type_of_items, items):
        """
        :param gen_info: contains info about the collection as a whole
        :param number_items: the number of items in the collection
        :param type_of_items: can be majority artworks or other misc items
        :param items: the list of items in the collection
        """
        self.title_of_collection = gen_info[0]
        self.date_of_auction = gen_info[1]
        self.time_of_auction = gen_info[2]
        self.place_of_auction = gen_info[3]
        self.number_of_items = number_items
        self.type_of_items = type_of_items
        self.items = items
        self.total_sale = None

    def print_gen_info(self):
        print('─' * 100)
        print(f'+ Title of Collection: {str(self.title_of_collection)}\n+ Date of Auction: {str(self.date_of_auction)}'
              f'\n+ Time of Auction: {str(self.time_of_auction)}\n+ Place of Auction: {str(self.place_of_auction)}'
              f'\n+ Number of items: {str(self.number_of_items)}\n+ Type of Items: {str(self.type_of_items)}'
              f'\n+ Total Sale: {str(self.total_sale)}')
        print('─' * 100)

    def print_type_item(self, type_of_items):
        if type_of_items == self.type_of_items:
            self.print_gen_info()
            self.print_item_info()

    def print_item_info(self):
        for item in self.items:
            print(item)

    def get_item_price(self):
        for item in self.items:
            print(item.price_number)

    def print_item_not_sold(self):
        count = 0
        for item in self.items:
            if item.price_number == "not sold":
                print(item)
                count += 1
        if count == 0:
            print("Collection is sold out!")

    def print_coll_total_sale_min(self, num: int, curr: str):
        c = CurrencyConverter()
        curr_total_sale = self.total_sale.split()
        new_price_point = c.convert(int(curr_total_sale[0]), curr_total_sale[1], curr)
        if new_price_point > num:
            self.print_gen_info()
            self.print_item_info()

    def accept(self, visitor: Visitor):
        return visitor.visit_collection(self)


class Item(SothebysObject):
    """
    A class for a specific item sold on the Sothebys website
    I is part of a collection of items
    """
    def __init__(self, index, title, price_number, price_currency, reserve_or_not, estimate_price_str):
        """
        The constructor of an Item
        :param index: item index in the collection
        :param title: name of item
        :param price_number: price value
        :param price_currency: currency used in the sale
        :param reserve_or_not: if the item has been reserved
        :param estimate_price_str: estimated price before sale
        """
        self.index = index
        self.title = title
        self.type = "Other items"
        self.price_number = price_number
        if price_number == 'not sold':
            self.price_currency = ""
        else:
            self.price_currency = price_currency
        self.reserve_or_not = reserve_or_not
        self.estimate_price = estimate_price_str

    def __str__(self):
        """:return: the string version of the Item defined below """
        return f"{self.index} - {self.title} - {self.type} - {self.price_number} {self.price_currency} - " \
               f"{self.reserve_or_not} - {self.estimate_price}"

    def accept(self, visitor: Visitor):
        return visitor.visit_item(self)


class ArtPiece(Item):
    """
        A specific type of Item with an author who made it
        """
    def __init__(self, index, author, title, price_number, price_currency, reserve_or_not, estimate_price_str):
        super().__init__(index, title, price_number, price_currency, reserve_or_not, estimate_price_str)
        self.author = author
        self.type = "Art pieces"

    def __str__(self):
        """
                The constructor of an Art Piece
                :param index: item index in the collection
                :param author: the artist who made it
                :param title: name of item
                :param price_number: price value
                :param price_currency: currency used in the sale
                :param reserve_or_not: if the item has been reserved
                :param estimate_price_str: estimated price before sale
                """
        return f"{self.index} - {self.author} - {self.title} - {self.type} - {self.price_number} {self.price_currency} " \
               f"- {self.reserve_or_not} - {self.estimate_price}"

    def accept(self, visitor: Visitor):
        return visitor.visit_art_piece(self)


# todo implement this class
class Currency(SothebysObject):
    def __init__(self, name):
        self.name = name
        pass

    def accept(self, visitor: Visitor):
        return visitor.visit_currency(self)


# todo implement this class
class Place(SothebysObject):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor: Visitor):
        return visitor.visit_place(self)
