from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    avatar = ProcessedImageField([ResizeToFill(100, 100),], upload_to='avatars', format='PNG', null=True, default=None)
    bio = models.TextField(max_length=500, null=True, blank=True)
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)

    points = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.first_name


WELCOME_MSG = '''
Hello %s,

Welcome to UIConnnect! Hope you have a nice time here.



UIConnect Team
'''


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        send_mail(
            'Welcome to UIConnect',
            WELCOME_MSG % instance.username,
            'uiconnectcsc303@gmail.com',
            [instance.email,],
            fail_silently=False
        )


post_save.connect(create_user_profile, sender=User)
