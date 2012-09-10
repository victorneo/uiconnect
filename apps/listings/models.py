from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFill
from categories.models import Category


class Listing(models.Model):
    user = models.ForeignKey(User, related_name='listings')
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2, help_text=u'Price in USD')
    is_featured = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, related_name="listings")

    def __unicode__(self):
        return self.name


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, related_name='images')
    image = models.ImageField(upload_to='listings', null=True, blank=True)
    caption = models.TextField(null=True, blank=True)
    formatted_image = ImageSpecField(
        [ResizeToFill(200, 200),],
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


def delete_thumbnail_images(sender, instance, **kwargs):
    instance.formatted_image.delete()
    instance.thumbnail.delete()
    instance.image.delete()


pre_delete.connect(delete_thumbnail_images, sender=ListingImage)
