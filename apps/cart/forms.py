from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Field
from crispy_forms.bootstrap import FormActions
from payments.models import Payment
from .models import Item


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('quantity',)


class PaymentForm(forms.ModelForm):
    discount_code = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('discount_code', css_class='span6'),
                Field('address', css_class='span9 delivery-address'),
            ),
            FormActions(
                HTML('<a class="btn" href="%s">Continue shopping</a> ' % kwargs.pop('cancel_url')),
                Submit('submit', 'Checkout', css_class='btn btn-success btn-checkout')
            )
        )
        super(PaymentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Payment
        fields = ('address',)
