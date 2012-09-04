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


class ListingImageForm(forms.Form):
    image1 = forms.ImageField(required=False)
    image2 = forms.ImageField(required=False)
    image3 = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                'image1',
                'image2',
                'image3',
            ),
            FormActions(
                Submit('submit', 'Upload', css_class='btn btn-primary')
            )
        )
        super(ListingImageForm, self).__init__(*args, **kwargs)
