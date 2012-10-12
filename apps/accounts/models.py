from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    avatar = ProcessedImageField([ResizeToFill(100, 100),], upload_to='avatars', format='PNG', null=True, blank=True, default=None)
    bio = models.TextField(max_length=500, null=True, blank=True)
    following = models.ManyToManyField('self', through='Relationship', related_name='followers', symmetrical=False)
    address = models.TextField(null=True, blank=True)

    alternate_login = models.BooleanField(default=False)
    fb_id = models.CharField(max_length=200, null=True, blank=True)

    points = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.first_name

    def add_relationship(self, profile):
        relationship, created = Relationship.objects.get_or_create(
            from_user=self,
            to_user=profile,
        )
        return relationship

    def remove_relationship(self, profile):
        Relationship.objects.filter(
            from_user=self,
            to_user=profile,
        ).delete()
        return

    def get_followers(self):
        return self.followers.filter(from_user__to_user=self).all()


class Relationship(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name='from_user')
    to_user = models.ForeignKey(UserProfile, related_name='to_user')


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
