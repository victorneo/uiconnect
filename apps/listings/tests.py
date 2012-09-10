import os
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from uiconnect import settings
from accounts.factories import UserFactory, UserProfileFactory
from categories.factories import CategoryFactory
from .factories import ListingFactory, ListingImageFactory
from .models import Listing, ListingImage


INDEX_URL = reverse('index')
ADD_URL = reverse('listings:add')


class ListingViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = UserFactory.build()
        self.user.set_password('1234')
        self.user.save()

        self.user2 = UserFactory.build()
        self.user2.set_password('1234')
        self.user2.save()

        self.l = ListingFactory(user=self.user)

        f = File(open(os.path.join(settings.SETTINGS_DIR, '..', 'static', 'tests', 'listing.jpg'), 'r'))
        self.img = ListingImageFactory(image=f, listing=self.l)
        f.close()

        self.c.login(username=self.user.username, password='1234')

    def test_index_template(self):
        response = self.c.get(INDEX_URL)
        self.assertTemplateUsed(response, 'index.html')
        self.assertTrue(response.context['categories'] != None)

    def test_view_template(self):
        url = reverse('listings:view', kwargs={'listing_id': self.l.id})
        response = self.c.get(url)
        self.assertTemplateUsed(response, 'listings/view.html')

    def test_view_invalid(self):
        url = reverse('listings:view', kwargs={'listing_id': 9999})
        response = self.c.get(url)
        self.assertEquals(404, response.status_code)

    def test_add_template(self):
        response = self.c.get(ADD_URL)
        self.assertTemplateUsed(response, 'listings/add.html')

    def test_add_invalid(self):
        data = {
            'name': '',
            'description': '',
            'price': 111,
        }

        response = self.c.post(ADD_URL)
        self.assertTemplateUsed(response, 'listings/add.html')

    def test_add_valid(self):
        category = CategoryFactory()
        data = {
            'name': 'ListingAddValid',
            'description': 'Desc for ListingAddValid',
            'price': 111,
            'categories': '%d' % category.id,
        }

        response = self.c.post(ADD_URL, data)

        self.assertEquals(1, Listing.objects.filter(name=data['name']).count())

        l = Listing.objects.get(name=data['name'])

        self.assertEquals(data['name'], l.name)
        self.assertEquals(data['description'], l.description)
        self.assertEquals(data['price'], l.price)
        self.assertRedirects(response, reverse('listings:manage_images', kwargs={'listing_id': l.id}))

    def test_manage_images_template(self):
        url = reverse('listings:manage_images', kwargs={'listing_id': self.l.id})
        response = self.c.get(url)
        self.assertTemplateUsed(response, 'listings/images.html')

    def test_manage_images_upload(self):
        url = reverse('listings:manage_images', kwargs={'listing_id': self.l.id})

        f = File(open(os.path.join(settings.SETTINGS_DIR, '..', 'static', 'tests', 'listing.jpg'), 'r'))
        data = {
            'img': f,
            'caption': 'Caption for image upload test',
        }

        response = self.c.post(url, data)

        l = Listing.objects.get(id=self.l.id)
        self.assertRedirects(response, url)
        self.assertEquals(2, l.images.count())

        img = l.images.all()[1]
        self.assertEquals(data['caption'], img.caption)
        img.delete()

        f.close()

    def test_manage_images_invalid_user(self):
        url = reverse('listings:manage_images', kwargs={'listing_id': self.l.id})
        self.c.logout()
        self.c.login(username=self.user2.username, password='1234')

        f = File(open(os.path.join(settings.SETTINGS_DIR, '..', 'static', 'tests', 'listing.jpg'), 'r'))
        data = {
            'img': f,
            'caption': 'Caption for image upload test',
        }

        response = self.c.post(url, data)
        self.assertRedirects(response, reverse('listings:view', kwargs={'listing_id': self.l.id}))

        f.close()

    def test_delete_image_valid(self):
        f = File(open(os.path.join(settings.SETTINGS_DIR, '..', 'static', 'tests', 'listing.jpg'), 'r'))
        img = ListingImageFactory(listing=self.l, image=f)

        url = reverse('listings:delete_image', kwargs={'listing_id': self.l.id, 'image_id': img.id})

        response = self.c.get(url)
        self.assertRedirects(response, reverse('listings:manage_images', kwargs={'listing_id': self.l.id}))
        self.assertEquals(1, ListingImage.objects.filter(listing=self.l).count())

    def test_delete_image_invalid(self):
        url = reverse('listings:delete_image', kwargs={'listing_id': self.l.id, 'image_id': 9999})
        response = self.c.get(url)
        self.assertRedirects(response, reverse('listings:manage_images', kwargs={'listing_id': self.l.id}))

    def test_update(self):
        url = reverse('listings:update', kwargs={'listing_id': self.l.id})
        response = self.c.get(url)
        self.assertTemplateUsed(response, 'listings/update.html')

    def test_update_invalid_user(self):
        self.c.logout()
        self.c.login(username=self.user2.username, password='1234')

        url = reverse('listings:update', kwargs={'listing_id': self.l.id})
        response = self.c.post(url, {'id': 'listing_name', 'value': ''})

        self.assertRedirects(response, reverse('listings:view', kwargs={'listing_id': self.l.id}))

    def test_delete(self):
        l = ListingFactory(user=self.user)
        url = reverse('listings:delete', kwargs={'listing_id': l.id})

        response = self.c.get(url)
        self.assertRedirects(response, reverse('index'))

    def test_delete_invalid_user(self):
        self.c.logout()
        self.c.login(username=self.user2.username, password='1234')

        url = reverse('listings:delete', kwargs={'listing_id': self.l.id})

        response = self.c.get(url)
        self.assertRedirects(response, reverse('listings:view', kwargs={'listing_id': self.l.id}))
