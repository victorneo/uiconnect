from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Field
from crispy_forms.bootstrap import FormActions
from .models import Listing


class AddListingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'description',
                'price',
            ),
            FormActions(
                Submit('submit', 'Add', css_class='btn btn-primary')
            )
        )
        super(AddListingForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Listing
        exclude = ('user',)


class AddImageForm(forms.Form):
    img = forms.ImageField()
    caption = forms.CharField(max_length=1000, required=False)
