from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from accounts.factories import UserFactory, UserProfileFactory
from listings.factories import ListingFactory, CollectionFactory
from listings.models import Listing
from paypal.standard.pdt.models import PayPalPDT
from .factories import PaymentFactory
from .models import Payment


PAYMENTS_URL = reverse('payments:index')


class PaymentsViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = UserFactory.build()
        self.user.set_password('1234')
        self.user.save()
        self.c.login(username=self.user.username, password='1234')

    def test_index_template(self):
        response = self.c.get(PAYMENTS_URL)
        self.assertTemplateUsed(response, 'payments/index.html')


class PaymentsUnitTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = UserFactory.build()
        self.user.set_password('1234')
        self.user.save()

        pdt = PayPalPDT(mc_gross=333, ipaddress='127.0.0.1', txn_id=123)
        pdt.save()

        self.payment = PaymentFactory(user=self.user, pdt=pdt)
        self.c.login(username=self.user.username, password='1234')

    def test_amount(self):
        self.assertEquals(333, self.payment.amount)

    def test_transaction_id(self):
        self.assertEquals(123, self.payment.transaction_id)

    def test_points_earned(self):
        self.assertEquals(33, self.payment.points_earned)

    def test_allocate_points(self):
        points = self.user.get_profile().points
        self.payment.allocate_points()
        self.assertEquals(points+self.payment.points_earned, self.user.get_profile().points)
