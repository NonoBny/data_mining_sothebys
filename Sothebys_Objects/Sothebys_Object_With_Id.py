from Sothebys_Objects.Sothebys_Objects import Artist, Collection, Item, ArtPiece, Currency, Place


class ArtistWithId(Artist):
    def __init__(self, artist: Artist, _id):
        super().__init__(artist.name, artist.life, artist.bio)
        self._id = _id


class CollectionWithId(Collection):
    def __init__(self, collection: Collection, _id):
        super().__init__([None, None, None, None], collection.number_of_items,
                         collection.type_of_items, collection.items)
        self.title_of_collection = collection.title_of_collection
        self.date_of_auction = collection.date_of_auction
        self.time_of_auction = collection.time_of_auction
        self.place_of_auction = collection.place_of_auction
        self._id = _id


class ItemWithId(Item):
    def __init__(self, item: Item, _id, collection_id):
        super().__init__(item.index, item.title, item.price_number,
                         item.price_currency, item.reserve_or_not, item.estimate_price)
        self._id = _id
        self.collection_id = collection_id


class ArtPieceWithId(ArtPiece):
    def __init__(self, art_piece: ArtPiece, _id):
        super().__init__(art_piece.index, art_piece.author, art_piece.title, art_piece.price_number,
                         art_piece.price_currency, art_piece.reserve_or_not, art_piece.estimate_price)


class CurrencyWithId(Currency):
    def __init__(self, currency: Currency, _id):
        super().__init__(currency.name)
        self._id = _id


class PlaceWithId(Place):
    def __init__(self, name, _id):
        super().__init__(name)
        self._id = _id
