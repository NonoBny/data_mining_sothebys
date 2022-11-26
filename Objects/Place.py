class Place:
    def __init__(self, name, country, city, address, phone_number):
        self.name = name
        self.country = country
        self.city = city
        self.address = address
        self.phone_number = phone_number

    def print(self):
        print(f'+ name: {str(self.name)}\n+ country: {str(self.country)}'
              f'\n+ city: {str(self.city)}\n+ address: {str(self.address)}'
              f'\n+ phone number: {str(self.phone_number)}')