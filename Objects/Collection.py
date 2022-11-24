from currency_converter import CurrencyConverter


class Collection:
    def __init__(self, gen_info, number_items, type_of_items, items):
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


class Item:
    def __init__(self, index, title, price_number, price_currency, reserve_or_not, estimate_price_str):
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
        return f"{self.index} - {self.title} - {self.type} - {self.price_number} {self.price_currency} - " \
               f"{self.reserve_or_not} - {self.estimate_price}"


class ArtPiece(Item):
    def __init__(self, index, author, title, price_number, price_currency, reserve_or_not, estimate_price_str):
        super().__init__(index, title, price_number, price_currency, reserve_or_not, estimate_price_str)
        self.author = author
        self.type = "Art pieces"

    def __str__(self):
        return f"{self.index} - {self.author} - {self.title} - {self.type} - {self.price_number} {self.price_currency} " \
               f"- {self.reserve_or_not} - {self.estimate_price}"
