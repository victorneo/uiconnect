from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from listings.models import Listing


class Cart(models.Model):
    user = models.OneToOneField(User, related_name='cart')
    listings = models.ManyToManyField(Listing)

    @property
    def total(self):
        total = 0
        for i in self.items.all():
            total += i.price

        return total

    @property
    def added_listings(self):
        listings = []
        for i in self.items.all():
            listings.append(i.listing)

        return listings

class Item(models.Model):
    cart = models.ForeignKey(Cart, related_name='items')
    listing = models.ForeignKey(Listing)
    quantity = models.IntegerField(default=1)

    @property
    def price(self):
        return self.listing.price * self.quantity


def create_cart(sender, instance, created, **kwargs):
    if created:
        cart = Cart(user=instance)
        cart.save()


post_save.connect(create_cart, sender=User)
