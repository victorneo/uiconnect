from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFill


class Listing(models.Model):
    user = models.ForeignKey(User, related_name='listings')
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, related_name='images')
    image = models.ImageField(upload_to='listings', null=True, blank=True)
    formatted_image = ImageSpecField(
        image_field='image',
        format='JPEG',
        options={'quality': 90}
    )
    thumbnail = ImageSpecField(
        [ResizeToFill(96, 96),],
        image_field='image',
        format='JPEG',
        options={'quality': 80}
    )


def create_listing_images(sender, instance, created, **kwargs):
    if created:
        for i in range(0, 3):
            ListingImage(listing=instance).save()


post_save.connect(create_listing_images, sender=Listing)
