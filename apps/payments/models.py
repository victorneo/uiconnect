from django.contrib.auth.models import User
from django.db import models
from paypal.standard.pdt.models import PayPalPDT
from listings.models import Listing


class Payment(models.Model):
    user = models.ForeignKey(User, related_name='payments')
    pdt = models.OneToOneField(PayPalPDT)

    @property
    def amount(self):
        return self.pdt.mc_gross

    @property
    def transaction_id(self):
        return self.pdt.txn_id

    @property
    def points_earned(self):
        return self.amount / 10

    def allocate_points(self):
        profile = self.user.get_profile()
        profile.points += self.points_earned
        profile.save()
