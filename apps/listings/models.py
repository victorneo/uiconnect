from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save, pre_delete
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFill
from categories.models import Category
from comments.models import Comment


class UpdateMixin(object):
    @property
    def update_type(self):
        return self.__class__.__name__


class Listing(models.Model, UpdateMixin):
    user = models.ForeignKey(User, related_name='listings')
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2, help_text=u'Price in USD')
    is_featured = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, related_name="listings")
    likes = models.ManyToManyField(User, related_name='liked_listings')
    comments = generic.GenericRelation(Comment)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    @property
    def last_liked_user(self):
        if self.likes.count() > 0:
            return self.likes.all()[self.likes.count()-1]
        else:
            return None


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


class Collection(models.Model, UpdateMixin):
    listings = models.ManyToManyField(Listing, related_name='collections')
    user = models.ForeignKey(User, related_name='collections')
    name = models.CharField(max_length=150)
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='liked_collections')
    image = models.ImageField(null=True, blank=True, upload_to='collections')
    comments = generic.GenericRelation(Comment)

    created_at = models.DateTimeField(auto_now_add=True)


def delete_thumbnail_images(sender, instance, **kwargs):
    instance.formatted_image.delete()
    instance.thumbnail.delete()
    instance.image.delete()


pre_delete.connect(delete_thumbnail_images, sender=ListingImage)
