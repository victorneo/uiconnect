import factory
from .models import Cart, Item


class CartFactory(factory.Factory):
    FACTORY_FOR = Cart


class ItemFactory(factory.Factory):
    FACTORY_FOR = Item

    quantity = 1
