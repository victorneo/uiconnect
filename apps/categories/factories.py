import factory
from .models import Category


class CategoryFactory(factory.Factory):
    FACTORY_FOR = Category

    name = factory.Sequence(lambda n: u'Category %s' % n)
    slug = factory.Sequence(lambda n: u'category-%s' % n)
