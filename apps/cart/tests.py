import os
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from uiconnect import settings
from accounts.factories import UserFactory, UserProfileFactory
from listings.factories import ListingFactory, ListingImageFactory
from listings.models import Listing
from .factories import ItemFactory


VIEW_URL = reverse('cart:view')


class CartViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = UserFactory.build()
        self.user.set_password('1234')
        self.user.save()

        self.user2 = UserFactory.build()
        self.user2.set_password('1234')
        self.user2.save()

        self.l = ListingFactory(user=self.user2)
        self.item = ItemFactory(cart=self.user.cart, listing=self.l)

        self.c.login(username=self.user.username, password='1234')

    def test_view(self):
        response = self.c.get(VIEW_URL)
        self.assertTemplateUsed(response, 'cart/view.html')
        self.assertEquals(1, response.context['cart'].items.count())

    def test_add_valid(self):
        l2 = ListingFactory(user=self.user2)
        url = reverse('cart:add', kwargs={'listing_id': l2.id})
        count = self.user.cart.items.count()

        response = self.c.post(url, {'quantity': 1})
        self.assertRedirects(response, reverse('listings:view', kwargs={'listing_id': l2.id}))
        self.assertEquals(count+1, self.user.cart.items.count())

    def test_add_invalid(self):
        url = reverse('cart:add', kwargs={'listing_id': 9999})
        response = self.c.post(url, {'quantity': 1})
        self.assertEquals(404, response.status_code)

    def test_add_own_item(self):
        self.c.login(username=self.user2.username, password='1234')
        count = self.user2.cart.items.count()
        url = reverse('cart:add', kwargs={'listing_id': self.l.id})
        response = self.c.post(url, {'quantity': 1})
        self.assertEquals(count, self.user2.cart.items.count())

    def test_remove_valid(self):
        l2 = ListingFactory(user=self.user2)
        item = ItemFactory(cart=self.user.cart, listing=l2)
        url = reverse('cart:remove', kwargs={'listing_id': l2.id})
        self.user.cart.items.add(item)
        count = self.user.cart.items.count()

        response = self.c.get(url)
        self.assertRedirects(response, VIEW_URL)
        self.assertEquals(count-1, self.user.cart.items.count())

    def test_remove_invalid_listing(self):
        url = reverse('cart:remove', kwargs={'listing_id': 9999})
        response = self.c.get(url)
        self.assertEquals(404, response.status_code)

    def test_remove_invalid_item(self):
        l2 = ListingFactory(user=self.user2)
        url = reverse('cart:remove', kwargs={'listing_id': l2.id})
        response = self.c.get(url)
        self.assertRedirects(response, VIEW_URL)


class CartUnitTest(TestCase):
    def setUp(self):
        self.user = UserFactory.build()
        self.user.set_password('1234')
        self.user.save()

        self.l = ListingFactory(user=self.user)
        self.item = ItemFactory(cart=self.user.cart, listing=self.l)

    def test_clear(self):
        self.assertEquals(1, self.user.cart.items.count())
        self.user.cart.clear()
        self.assertEquals(0, self.user.cart.items.count())
