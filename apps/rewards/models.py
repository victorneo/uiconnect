from django.contrib.auth.models import User
from django.db import models
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFill


class Reward(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    points_required = models.IntegerField(default=0)
    image = models.ImageField(upload_to='rewards', null=True, blank=True)
    formatted_image = ImageSpecField(
        [ResizeToFill(200, 200),],
        image_field='image',
        format='JPEG',
        options={'quality': 90}
    )
    redeemed_by = models.ManyToManyField(User, related_name='redeemed_rewards')
