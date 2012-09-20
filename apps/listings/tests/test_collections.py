import os
import json
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from uiconnect import settings
from accounts.factories import UserFactory, UserProfileFactory
from categories.factories import CategoryFactory
from listings.factories import ListingFactory, ListingImageFactory, CollectionFactory
from listings.models import Listing, Collection


INDEX_URL = reverse('collections:index')
ADD_URL = reverse('collections:add')


class CollectionViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = UserFactory.build()
        self.user.set_password('1234')
        self.user.save()

        self.l = ListingFactory(user=self.user)
        self.l2 = ListingFactory(user=self.user)
        self.c.login(username=self.user.username, password='1234')

        self.c1 = CollectionFactory(user=self.user, is_featured=True)
        self.c2 = CollectionFactory(user=self.user)

    def test_index(self):
        response = self.c.get(INDEX_URL)
        self.assertTemplateUsed(response, 'collections/collections.html')

        self.assertTrue(response.context['collections'] != None)
        self.assertEquals(self.c1, response.context['collections'][0])

        response = self.c.get(INDEX_URL + '?type=new')
        self.assertEquals(self.c2, response.context['collections'][0])

    def test_view_collection_template(self):
        url = reverse('collections:view', kwargs={'collection_id': self.c1.id})
        response = self.c.get(url)
        self.assertTemplateUsed(response, 'collections/view.html')

    def test_like(self):
        url = reverse('collections:like', kwargs={'collection_id': self.c1.id})
        self.c.login(username=self.user.username, password='1234')

        response = self.c.get(url)
        self.assertTrue(json.loads(response.content)['success'])
        self.assertEquals(1, self.c1.likes.count())

        response = self.c.get(url)
        self.assertTrue(json.loads(response.content)['success'])
        self.assertEquals(0, self.c1.likes.count())

    def test_like_invalid_collection(self):
        url = reverse('collections:like', kwargs={'collection_id': 9999})
        self.c.login(username=self.user.username, password='1234')

        response = self.c.get(url)
        self.assertFalse(json.loads(response.content)['success'])

    def test_add_collection_template(self):
        self.c.login(username=self.user.username, password='1234')
        response = self.c.get(ADD_URL)
        self.assertTemplateUsed(response, 'collections/add.html')

    def test_add_collection_valid(self):
        self.c.login(username=self.user.username, password='1234')
        data = {'name': 'Col 1', 'description': 'Desc 1'}
        response = self.c.post(ADD_URL, data)

        self.assertEquals(1, Collection.objects.filter(name='Col 1').count())
        c3 = Collection.objects.get(name='Col 1')

        self.assertRedirects(response, reverse('collections:add_listings',
                             kwargs={'collection_id': c3.id}))
        self.assertEquals(data['name'], c3.name)
        self.assertEquals(data['description'], c3.description)

    def test_add_collection_invalid(self):
        self.c.login(username=self.user.username, password='1234')
        data = {'name': '', 'description': 'Desc 1'}
        response = self.c.post(ADD_URL, data)

        self.assertTemplateUsed(response, 'collections/add.html')

    def test_add_collection_listings_template(self):
        url = reverse('collections:add_listings', kwargs={'collection_id': self.c1.id})
        self.c.login(username=self.user.username, password='1234')

        response = self.c.get(url)
        self.assertTemplateUsed(response, 'collections/add_listings.html')

    def test_add_collection_listings_valid(self):
        url = reverse('collections:add_listings', kwargs={'collection_id': self.c1.id})
        self.c.login(username=self.user.username, password='1234')

        response = self.c.post(url, {'listings': '%d' %(self.l.id)})
        self.assertRedirects(response, reverse('collections:view', kwargs={'collection_id': self.c1.id}))
        self.assertEquals(1, self.c1.listings.count())
        self.assertEquals(self.l.id, self.c1.listings.get().id)

        response = self.c.post(url, {'listings': '%d' %(self.l2.id)})
        self.assertRedirects(response, reverse('collections:view', kwargs={'collection_id': self.c1.id}))
        self.assertEquals(1, self.c1.listings.count())
        self.assertEquals(self.l2.id, self.c1.listings.get().id)

    def test_update_collection_template(self):
        self.c.login(username=self.user.username, password='1234')
        data = {'name': '', 'description': 'Desc 1'}
        response = self.c.post(ADD_URL, data)

        self.assertTemplateUsed(response, 'collections/add.html')
