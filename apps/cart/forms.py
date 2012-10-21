from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Field
from crispy_forms.bootstrap import FormActions
from .models import Cart, Item


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('quantity',)


class CartForm(forms.ModelForm):
    discount_code = forms.CharField(required=False, help_text=u'Use any discount code you have here.')
    address = forms.CharField(
            required=True,
            widget=forms.Textarea,
            help_text=u'Enter the full address for the items to be delivered to, including the Country.')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('discount_code', css_class='span4'),
                Field('address', css_class='span9 delivery-address'),
            ),
            FormActions(
                HTML('<a class="btn" href="%s">Continue shopping</a> ' % kwargs.pop('cancel_url')),
                Submit('submit', 'Proceed to Checkout', css_class='btn btn-primary btn-checkout')
            )
        )
        super(CartForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Cart
        fields = ('address', 'discount_code')
