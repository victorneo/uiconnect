from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from paypal.standard.pdt.models import PayPalPDT
from listings.models import Listing


class Payment(models.Model):
    user = models.ForeignKey(User, related_name='payments')
    pdt = models.OneToOneField(PayPalPDT, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    address = models.TextField()
    listings = models.ManyToManyField(Listing, related_name='payments', through='PaymentItem')

    def __init__(self, *args, **kwargs):
        # cache total
        self.total = None
        super(Payment, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return '%s, is paid: %s' % (str(self.user), self.is_paid)

    @property
    def amount_due(self):
        if self.total:
            return self.total

        total = Decimal(0.0)
        for l in self.listings.all():
            total += l.paymentitem_set.get(payment=self).price

        try:
            discounted_amt = self.discount.percentage * (total / 100)
        except Discount.DoesNotExist:
            pass
        else:
            total -= discounted_amt

        self.total = total
        return total

    @property
    def amount_paid(self):
        return self.pdt.mc_gross

    @property
    def transaction_id(self):
        return self.pdt.txn_id

    @property
    def points_earned(self):
        return int(self.amount_paid / 10)

    @property
    def payment_date(self):
        return self.pdt.payment_date

    def allocate_points(self):
        profile = self.user.get_profile()
        profile.points += self.points_earned
        profile.save()


class PaymentItem(models.Model):
    listing = models.ForeignKey(Listing)
    payment = models.ForeignKey(Payment)
    quantity = models.IntegerField(default=1)

    @property
    def price(self):
        return Decimal(self.listing.price * self.quantity)


class Discount(models.Model):
    user = models.ForeignKey(User, related_name='discounts')
    code = models.CharField(max_length=50, unique=True)
    percentage = models.DecimalField(decimal_places=2, max_digits=3)
    payment = models.OneToOneField(Payment, related_name='discount', blank=True, null=True, on_delete=models.SET_NULL)
