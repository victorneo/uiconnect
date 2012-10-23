import os
import json
from django.core import mail
from django.core.files import File
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
import requests
import mock
from uiconnect import settings
from .backends import FacebookBackend, PersonaBackend
from .factories import UserFactory, UserProfileFactory


LOGIN_URL = reverse('accounts:login')
LOGOUT_URL = reverse('accounts:logout')
REGISTER_URL = reverse('accounts:register')
PROFILE_URL = reverse('accounts:profile')
FORGOT_PASSWORD_URL = reverse('accounts:forgot_password')
FOLLOWING_URL = reverse('accounts:following')


class AccountsViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = UserFactory.build()
        self.user.set_password('1234')
        self.user.save()

        f = File(open(os.path.join(settings.SETTINGS_DIR, '..', 'static', 'tests', 'avatar.jpg'), 'r'))
        self.user.get_profile().avatar = f
        self.user.get_profile().save()
        f.close()

        self.user2 = UserFactory.build()
        self.user2.set_password('1234')
        self.user2.save()

        mail.outbox = []

    def test_login_template(self):
        response = self.c.get(LOGIN_URL)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_valid(self):
        response = self.c.post(LOGIN_URL, {'username': self.user.username, 'password': '1234'})
        self.assertRedirects(response, reverse('dashboard'))
        self.c.logout()

    def test_login_invalid(self):
        response = self.c.post(LOGIN_URL, {'username': self.user.username, 'password': 'password'})
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_already_logged_in(self):
        self.c.login(username=self.user.username, password='1234')
        response = self.c.get(LOGIN_URL)
        self.assertRedirects(response, reverse('dashboard'))
        self.c.logout()

    def test_logout(self):
        self.c.login(username=self.user.username, password='1234')
        response = self.c.get(LOGOUT_URL)
        self.assertNotIn('_auth_user_id', self.c.session)

    def test_register_template(self):
        response = self.c.get(REGISTER_URL)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_valid(self):
        data = {
            'name': 'New User',
            'username': 'newuser',
            'password': '12345',
            'password2': '12345',
            'email': 'new@user.com',
            'bio': 'a new user',
            'avatar': '',
        }
        response = self.c.post(REGISTER_URL, data)

        self.assertEquals(1, User.objects.filter(username='newuser').count())
        u = User.objects.get(username='newuser')

        self.assertEquals(data['username'], u.username)
        self.assertEquals(data['email'], u.email)
        self.assertEquals(data['bio'], u.get_profile().bio)
        self.assertTrue(authenticate(username=data['username'], password=data['password']))

    def test_register_invalid(self):
        data = {
            'name': 'New User',
            'username': 'newuser',
            'password': '12345',
            'password2': '1234',
            'email': 'new@user.com',
            'bio': 'a new user',
            'avatar': '',
        }
        response = self.c.post(REGISTER_URL, data)

        self.assertEquals(0, User.objects.filter(username='newuser').count())
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertContains(response, u'Passwords are not the same.')

    def test_register_username_taken(self):
        UserFactory(username='takenuser')
        data = {
            'name': 'Taken User',
            'username': 'takenuser',
            'password': '12345',
            'password2': '12345',
            'email': 'new@user.com',
            'bio': 'a new user',
            'avatar': '',
        }
        response = self.c.post(REGISTER_URL, data)

        self.assertEquals(1, User.objects.filter(username='takenuser').count())
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertContains(response, u'Username has been taken.')

    def test_profile_template(self):
        self.c.login(username=self.user.username, password='1234')
        response = self.c.get(PROFILE_URL)

        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.c.logout()

    def test_profile_template_hide_password(self):
        self.c.login(username=self.user.username, password='1234')
        self.user.get_profile().alternate_login = True
        self.user.get_profile().save()
        response = self.c.get(PROFILE_URL)

        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertContains(response, 'input id="id_password" type="hidden"')
        self.assertContains(response, 'input id="id_password2" type="hidden"')
        self.c.logout()

    def test_profile_valid_update(self):
        self.c.login(username=self.user.username, password='1234')
        f = File(open(os.path.join(settings.SETTINGS_DIR, '..', 'static', 'tests', 'new_avatar.jpg'), 'r'))

        data = {
            'name': 'New Name',
            'password': 'abcd',
            'password2': 'abcd',
            'email': 'asd@asd.com',
            'bio': 'New Bio for New Name',
            'avatar': f,
            'converted_currency': 'SGD',
            'address': 'Somewhere',
        }

        response = self.c.post(PROFILE_URL, data)
        u = User.objects.get(username=self.user.username)

        self.assertRedirects(response, PROFILE_URL)
        self.assertEquals(data['name'], u.first_name)
        self.assertEquals(data['email'], u.email)
        self.assertEquals(data['bio'], u.get_profile().bio)
        self.assertEquals(data['converted_currency'], u.get_profile().default_currency)
        self.assertEquals(data['address'], u.get_profile().address)
        self.assertTrue(authenticate(username=self.user.username, password=data['password']))

    def test_profile_valid_update_clear_avatar(self):
        self.c.login(username=self.user.username, password='1234')

        data = {
            'name': 'New Name',
            'password': 'abcd',
            'password2': 'abcd',
            'email': 'asd@asd.com',
            'bio': 'New Bio for New Name',
            'avatar': '',
            'converted_currency': 'SGD',
            'avatar-clear': True,
        }

        response = self.c.post(PROFILE_URL, data)
        u = User.objects.get(username=self.user.username)

        self.assertEquals(u'', u.get_profile().avatar.name)

    def test_profile_invalid_update(self):
        self.c.login(username=self.user.username, password='1234')

        data = {
            'name': 'New Name',
            'password': 'abcd',
            'password2': 'abc',
            'email': '',
            'bio': 'New Bio for New Name',
            'converted_currency': 'SGD',
            'avatar': '',
        }

        response = self.c.post(PROFILE_URL, data)
        self.assertTemplateUsed(response, 'accounts/profile.html')

        self.c.logout()

    def test_forgot_password_template(self):
        response = self.c.get(FORGOT_PASSWORD_URL)

        self.assertTemplateUsed(response, 'accounts/forgot_password.html')

    def test_forgot_password_invalid_email(self):
        response = self.c.post(FORGOT_PASSWORD_URL, {'username': 'haha'})

        self.assertTemplateUsed(response, 'accounts/forgot_password.html')
        self.assertContains(response, u'Invalid username.')

    def test_forgot_password_valid(self):
        response = self.c.post(FORGOT_PASSWORD_URL, {'username': self.user.username})

        self.assertRedirects(response, LOGIN_URL)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, u'Your temporary password')

    def test_follow(self):
        url = reverse('accounts:follow', kwargs={'user_id': self.user2.id})
        self.c.login(username=self.user.username, password='1234')

        response = self.c.get(url)
        self.assertTrue(json.loads(response.content)['success'])
        self.assertEquals(1, self.user2.get_profile().get_followers().count())

        response = self.c.get(url)
        self.assertEquals(0, self.user2.get_profile().get_followers().count())

    def test_follow_ownself(self):
        url = reverse('accounts:follow', kwargs={'user_id': self.user.id})
        self.c.login(username=self.user.username, password='1234')

        response = self.c.get(url)
        self.assertFalse(json.loads(response.content)['success'])
        self.assertEquals(0, self.user.get_profile().followers.count())

    def test_follow_invalid_user(self):
        url = reverse('accounts:follow', kwargs={'user_id': 9999})
        self.c.login(username=self.user.username, password='1234')

        response = self.c.get(url)
        self.assertFalse(json.loads(response.content)['success'])

    def test_following_template(self):
        self.c.login(username=self.user.username, password='1234')

        self.user.get_profile().add_relationship(self.user2.get_profile())
        self.user.get_profile().save()

        response = self.c.get(FOLLOWING_URL)
        self.assertTemplateUsed(response, 'accounts/following.html')
        self.assertEquals(1, response.context['following_users'].count())

    def test_unfollow(self):
        url = reverse('accounts:unfollow', kwargs={'user_id': self.user2.id})
        self.c.login(username=self.user.username, password='1234')

        self.user2.get_profile().add_relationship(self.user.get_profile())
        self.user2.get_profile().save()

        response = self.c.get(url)
        self.assertEquals(0, self.user2.get_profile().followers.count())
        self.assertRedirects(response, FOLLOWING_URL)

    def test_unfollow_invalid_user(self):
        url = reverse('accounts:unfollow', kwargs={'user_id': 9999})
        self.c.login(username=self.user.username, password='1234')

        response = self.c.get(url)
        self.assertRedirects(response, FOLLOWING_URL)

    def test_view_valid_profile(self):
        url = reverse('accounts:view_profile', kwargs={'user_id': self.user.id})
        response = self.c.get(url)

        self.assertTemplateUsed(response, 'accounts/view.html')

    def test_view_invalid_profile(self):
        url = reverse('accounts:view_profile', kwargs={'user_id': 9999})
        response = self.c.get(url)

        self.assertEquals(404, response.status_code)

    def test_avatar_valid(self):
        url = reverse('accounts:avatar')
        response = self.c.get(url + '?username=%s' % self.user.username)

        data = json.loads(response.content)
        self.assertEquals(self.user.get_profile().avatar.url, data['url'])

    def test_avatar_invalid(self):
        url = reverse('accounts:avatar')
        response = self.c.get(url + '?username=ahhahahahaha')

        self.assertEquals('', response.content)


class AccountsFacebookBackendUnitTest(TestCase):
    def setUp(self):
        self.user = UserFactory.build()
        self.user.set_password('1234')
        self.user.save()

        p = self.user.get_profile()
        p.fb_id = '1234567'
        p.save()

        self.backend = FacebookBackend()

    def test_authenticate_valid(self):
        self.assertEquals(self.user, self.backend.authenticate(fb_id='1234567'))

    def test_authenticate_invalid(self):
        self.assertEquals(None, self.backend.authenticate(fb_id='asd'))

    def test_get_user_valid(self):
        self.assertEquals(self.user, self.backend.get_user(user_id=self.user.id))

    def test_get_user_invalid(self):
        self.assertEquals(None, self.backend.get_user(user_id=1234))


class RequestResponse(object):
    pass


def requests_post(url, data, verify=False):
    obj = RequestResponse()
    out_data = {'status': 'okay', 'email': 'persona@user.com'}
    if data['assertion'] == '12345678':
        obj.ok = True
        obj.content = str(json.JSONEncoder().encode(out_data))
    else:
        obj.ok = False

    return obj


class AccountsPersonaBackendUnitTest(TestCase):
    def setUp(self):
        self.user = UserFactory.build(email='persona@user.com')
        self.user.set_password('1234')
        self.user.save()

        p = self.user.get_profile()
        p.alternate_login = True
        p.save()

        self.backend = PersonaBackend()

    def test_authenticate_valid(self):
        with mock.patch.object(requests, 'post', requests_post):
            self.assertEquals(self.user, self.backend.authenticate(assertion='12345678'))

    def test_authenticate_valid_create_new(self):
        self.user.delete()
        with mock.patch.object(requests, 'post', requests_post):
            self.assertEquals('persona@user.com', self.backend.authenticate(assertion='12345678').email)

    def test_authenticate_invalid(self):
        with mock.patch.object(requests, 'post', requests_post):
            self.assertEquals(None, self.backend.authenticate(assertion='asd'))

    def test_get_user_valid(self):
        with mock.patch.object(requests, 'post', requests_post):
            self.assertEquals(self.user, self.backend.get_user(user_id=self.user.id))

    def test_get_user_invalid(self):
        with mock.patch.object(requests, 'post', requests_post):
            self.assertEquals(None, self.backend.get_user(user_id=1234))
