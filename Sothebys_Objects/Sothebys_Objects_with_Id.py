from Sothebys_Objects.Sothebys_Objects import SothebysObject, Collection, Item, ArtPiece, Artist, Currency, Place


# a decorator to add ids to previous objects
class SothebysObjectWithId(SothebysObject):
    def __init__(self, sothebys_object: SothebysObject, _id):
        self.sothebys_object = sothebys_object
        self._id = _id


class CollectionWithId(Collection):
    def __init__(self, collection: Collection, _id):
        gen_info = [collection.title_of_collection,
                    collection.date_of_auction,
                    collection.time_of_auction,
                    collection.place_of_auction]
        super().__init__(gen_info, collection.number_of_items, collection.type_of_items, collection.items)
        self.unique_id = _id
        _i_id = 1

        items_with_ids = []
        for item in collection.items:
            item_id = 1000*self.unique_id + _i_id
            if type(item) is ArtPiece:
                item_with_id = ArtPieceWithId(item, item_id, self.unique_id)
            else:
                item_with_id = ItemWithId(item, item_id, self.unique_id)
            items_with_ids.append(item_with_id)
            _i_id += 1
        self.items = items_with_ids


class ItemWithId(Item):
    def __init__(self, item: Item, _id, _parent_id):
        super().__init__(item.index, item.title, item.price_number, item.price_currency, item.reserve_or_not, item.estimate_price)
        self.parent_id = _parent_id
        self.unique_id = _id


class ArtPieceWithId(ArtPiece):
    def __init__(self, art_piece: ArtPiece, _id, _parent_id):
        super().__init__(art_piece.index, art_piece.author, art_piece.title, art_piece.price_number,
                         art_piece.price_currency, art_piece.reserve_or_not, art_piece.estimate_price)
        self.parent_id = _parent_id
        self.unique_id = _id


class ArtistWithId(Artist):
    def __init__(self, artist: Artist, _id):
        super().__init__(artist.name, artist.life, artist.bio)
        self.unique_id = _id


class CurrencyWithId(Currency):
    def __init__(self, currency: Currency, _id):
        super().__init__(currency.name)
        self.unique_id = _id


class PlaceWithId(Place):
    def __init__(self, place: Place, _id):
        super().__init__(place.region_name, place.city, place.address, place.phone_number, place.bio)
        self.unique_id = _id
