import binascii
import os
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db import models
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFill
from payments.models import Discount


REWARD_TYPES = (
        ('V', 'Voucher'),
        ('D', 'Discount'),
    )


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
    reward_type = models.CharField(max_length=1, default='V' ,choices=REWARD_TYPES)

    # for discount rewards only, don't normalize fully
    percentage = models.IntegerField(default=0)

    def redeem(self, profile):
        if profile.points < self.points_required:
            raise Exception('Insufficient Points')

        self.redeemed_by.add(profile.user)
        self.save()

        profile.points -= self.points_required
        profile.save()

        # probably can rewrite this as a signal
        # discount redeemed
        if self.reward_type == 'D':
            while True:
                code = binascii.b2a_hex(os.urandom(10))
                if Discount.objects.filter(code=code, user=profile.user).count() == 0:
                    break

            discount = Discount(user=profile.user, code=code, percentage=self.percentage)
            discount.save()

            send_mail(
                'Code for Discount',
                '%s' % code,
                'uiconnect303@gmail.com',
                [profile.user.email,]
            )

    def __unicode__(self):
        return u'%s (%d points)' % (self.name, self.points_required)
