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
