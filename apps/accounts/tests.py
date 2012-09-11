import os
from django.core import mail
from django.core.files import File
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from uiconnect import settings
from .factories import UserFactory, UserProfileFactory


LOGIN_URL = reverse('accounts:login')
LOGOUT_URL = reverse('accounts:logout')
REGISTER_URL = reverse('accounts:register')
PROFILE_URL = reverse('accounts:profile')
FORGOT_PASSWORD_URL = reverse('accounts:forgot_password')


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

        mail.outbox = []

    def test_login_template(self):
        response = self.c.get(LOGIN_URL)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_valid(self):
        response = self.c.post(LOGIN_URL, {'username': self.user.username, 'password': '1234'})
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_invalid(self):
        response = self.c.post(LOGIN_URL, {'username': self.user.username, 'password': 'password'})
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_logout(self):
        self.c.login(username=self.user.username, password='1234')
        response = self.c.get(LOGOUT_URL)
        self.assertNotIn('_auth_user_id', self.c.session)

    def test_register_template(self):
        response = self.c.get(REGISTER_URL)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_valid(self):
        data = {
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
        }

        response = self.c.post(PROFILE_URL, data)
        u = User.objects.get(username=self.user.username)

        self.assertRedirects(response, PROFILE_URL)
        self.assertEquals(data['name'], u.first_name)
        self.assertEquals(data['email'], u.email)
        self.assertEquals(data['bio'], u.get_profile().bio)
        self.assertTrue(authenticate(username=self.user.username, password=data['password']))

    def test_profile_invalid_update(self):
        self.c.login(username=self.user.username, password='1234')

        data = {
            'name': 'New Name',
            'password': 'abcd',
            'password2': 'abcd',
            'email': '',
            'bio': 'New Bio for New Name',
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
