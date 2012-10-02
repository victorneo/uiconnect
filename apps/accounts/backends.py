import json
import requests
from django.contrib.auth.models import User
from .models import UserProfile


class FacebookBackend(object):
    def authenticate(self, fb_id=None):
        try:
            user = UserProfile.objects.get(fb_id=fb_id).user
            return user
        except UserProfile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class PersonaBackend(object):
    def authenticate(self, assertion=None):
        # Send the assertion to Mozilla's verifier service.
        data = {'assertion': assertion, 'audience': 'http://127.0.0.1:8000'}
        resp = requests.post('https://verifier.login.persona.org/verify', data=data, verify=True)

        # Did the verifier respond?
        if resp.ok:
            # Parse the response
            verification_data = json.loads(resp.content)

            # Check if the assertion was valid
            if verification_data['status'] == 'okay':
                return self.get_user_or_create(verification_data['email'])

        return None

    def get_user_or_create(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(username=email,
                                            password='',
                                            email=email)
            user.first_name = email.split('@')[0]
            user.save()

            user.get_profile().alternate_login = True
            user.get_profile().save()

        print user

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
