import factory
from mock import Mock
from .models import Payment


class PaymentFactory(factory.Factory):
    FACTORY_FOR = Payment
