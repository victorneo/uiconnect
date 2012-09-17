from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from accounts.factories import UserFactory, UserProfileFactory
from listings.factories import ListingFactory, CollectionFactory
from listings.models import Listing


SEARCH_URL = reverse('search:results')


class SearchTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = UserFactory.build()
        self.user.set_password('1234')
        self.user.save()

        self.l = ListingFactory(user=self.user, name='Listing Alpha')
        self.c1 = CollectionFactory(user=self.user, name='Collection Alpha')

        self.c.login(username=self.user.username, password='1234')

    def test_search(self):
        data = {'query': 'Alpha', 'search_type': 'all'}
        response = self.c.post(SEARCH_URL, data)

        self.assertTemplateUsed(response, 'search/results.html')
        self.assertEquals(1, response.context['listings'].count())
        self.assertEquals(1, response.context['collections'].count())

        data = {'query': 'Alpha', 'search_type': 'listing'}
        response = self.c.post(SEARCH_URL, data)
        self.assertEquals(1, response.context['listings'].count())
        self.assertEquals(None, response.context['collections'])

        data = {'query': 'Alpha', 'search_type': 'collection'}
        response = self.c.post(SEARCH_URL, data)
        self.assertEquals(None, response.context['listings'])
        self.assertEquals(1, response.context['collections'].count())

        data = {'query': 'Beta', 'search_type': 'all'}
        response = self.c.post(SEARCH_URL, data)
        self.assertEquals(0, response.context['listings'].count())
        self.assertEquals(0, response.context['collections'].count())

        data = {'query': '', 'search_type': 'all'}
        response = self.c.post(SEARCH_URL, data)
        self.assertEquals(None, response.context['listings'])
        self.assertEquals(None, response.context['collections'])
