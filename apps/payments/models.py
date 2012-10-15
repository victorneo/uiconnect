from django.contrib.auth.models import User
from django.db import models
from paypal.standard.pdt.models import PayPalPDT
from listings.models import Listing


class Payment(models.Model):
    user = models.ForeignKey(User, related_name='payments')
    pdt = models.OneToOneField(PayPalPDT, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    address = models.TextField()
    listings = models.ManyToManyField(Listing, related_name='payments')

    @property
    def amount(self):
        return self.pdt.mc_gross

    @property
    def transaction_id(self):
        return self.pdt.txn_id

    @property
    def points_earned(self):
        return int(self.amount / 10)

    @property
    def payment_date(self):
        return self.pdt.payment_date

    def allocate_points(self):
        profile = self.user.get_profile()
        profile.points += self.points_earned
        profile.save()


class Discount(models.Model):
    user = models.ForeignKey(User, related_name='discounts')
    code = models.CharField(max_length=50, unique=True)
    percentage = models.DecimalField(decimal_places=2, max_digits=3)
    payment = models.OneToOneField(Payment, related_name='discount', blank=True, null=True, on_delete=models.SET_NULL)
