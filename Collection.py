class Collection:
    def __init__(self, gen_info, number_items, type_of_items, items):
        self.title_of_collection = gen_info[0]
        self.date_of_auction = gen_info[1]
        self.time_of_auction = gen_info[2]
        self.place_of_auction = gen_info[3]
        self.number_of_items = number_items
        self.type_of_Items = type_of_items
        self.items = items
        self.total_sale = None

    def print(self):
        print('─' * 100)
        print(f'+ Title of Collection: {str(self.title_of_collection)}\n+ Date of Auction: {str(self.date_of_auction)}'
              f'\n+ Time of Auction: {str(self.time_of_auction)}\n+ Place of Auction: {str(self.place_of_auction)}'
              f'\n+ Number of items: {str(self.number_of_items)}\n+ Type of Items: {str(self.type_of_Items)}'
              f'\n+ Total Sale: {str(self.total_sale)}')
        print('─' * 100)
        for item in self.items:
            print(item)


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
