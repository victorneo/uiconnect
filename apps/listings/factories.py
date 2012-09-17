import factory
from .models import Listing, ListingImage, Collection


class ListingFactory(factory.Factory):
    FACTORY_FOR = Listing

    name = factory.Sequence(lambda n: u'Listing %s' % n)
    description = factory.Sequence(lambda n: u'This is listing %s' % n)
    price = 500.00


class ListingImageFactory(factory.Factory):
    FACTORY_FOR = ListingImage

    caption = factory.Sequence(lambda n: 'Caption for image %s' % n)

class CollectionFactory(factory.Factory):
    FACTORY_FOR = Collection

    name = factory.Sequence(lambda n: u'Collection %s' % n)
    description = factory.Sequence(lambda n: u'This is collection %s' % n)
