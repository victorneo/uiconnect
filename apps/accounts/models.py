from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    avatar = ProcessedImageField([ResizeToFill(100, 100),], upload_to='avatars', format='PNG', null=True, default=None)
    bio = models.TextField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return self.user.first_name


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)
