from django.contrib.auth.models import User
from django.db import models
from django.db.models import post_save

from listings.models import Listing


class Cart(models.Model):
    user = models.OneToOneField(User, related_name='cart')
    listings = models.ManyToManyField(Listing)


class Item(models.Model):
    cart = models.ForeignKey(Cart, related_name='items')
    item = models.ForeignKey(Listing)
    quantity = models.IntegerField()


def create_cart(sender, instance, created, **kwargs):
    if created:
        cart = Cart(user=instance)
        cart.save()


post_save.connect(create_cart, sender=User)
