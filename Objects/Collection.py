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
        print('title of collection: ' + str(self.title_of_collection))
        print('date and time of auction: ' + str(self.date_of_auction) + ', ' + str(self.time_of_auction))
        print('location: ' + str(self.place_of_auction))
        print('number of item: ' + str(self.number_of_items))
        print('type of items: ' + str(self.type_of_Items))
        print('total sale: ' + str(self.total_sale))


class Item:
    def __init__(self, index, title, price_number, price_currency, reserve_or_not, estimate_price_str):
        self.index = index
        self.title = title
        self.type = "Other items"
        self.price_number = price_number
        self.price_currency = price_currency
        self.reserve_or_not = reserve_or_not
        self.estimate_price = estimate_price_str

    def print(self):
        print('\t' + 'item number: ' + str(self.index))
        print('\t' + 'title of item : ' + str(self.title))
        print('\t' + 'type of item: ' + str(self.type))
        print('\t' + 'price: ' + str(self.price_number) + ' ' + str(self.price_currency))
        print('\t' + 'reserved: ' + str(self.reserve_or_not))
        print('\t' + 'estimated price: ' + str(self.estimate_price))
        print('\n')


class ArtPiece(Item):
    def __init__(self, index, author, title, price_number, price_currency, reserve_or_not, estimate_price_str):
        super().__init__(index, title, price_number, price_currency, reserve_or_not, estimate_price_str)
        self.author = author
        self.type = "Art pieces"

    def print(self):
        print('\t' + 'item number: ' + str(self.index))
        print('\t' + 'author: ' + str(self.author))
        print('\t' + 'title of art piece : ' + str(self.title))
        print('\t' + 'type of item: ' + str(self.type))
        print('\t' + 'price: ' + str(self.price_number + ' ' + self.price_currency))
        print('\t' + 'reserved: ' + str(self.reserve_or_not))
        print('\t' + 'estimated price: ' + str(self.estimate_price))
        print('\n')
