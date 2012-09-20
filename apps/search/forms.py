from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Field
from crispy_forms.bootstrap import FormActions


class SearchForm(forms.Form):
    SEARCH_TYPE_CHOICES = (
        ('all', 'All'),
        ('collection', 'Collections only'),
        ('listing', 'Listings only'),
    )

    query = forms.CharField(max_length=200, required=True)
    search_type = forms.ChoiceField(choices=SEARCH_TYPE_CHOICES, required=True)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('query', css_class='span6'),
                Field('search_type', css_class='span6'),
            ),
            FormActions(
                Submit('submit', 'Go', css_class='btn btn-primary')
            )
        )
        super(SearchForm, self).__init__(*args, **kwargs)
