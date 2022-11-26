import currency_converter


class Currency:
    def __init__(self, name):
        self.name = name
        c = currency_converter.CurrencyConverter()
        self.dollar_value = c.convert(1, name, 'USD')

    def print(self):
        print(f'+ currency: {str(self.name)}\n+ dollar_value {str(self.dollar_value)}')
