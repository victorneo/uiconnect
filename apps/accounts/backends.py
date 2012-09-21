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
