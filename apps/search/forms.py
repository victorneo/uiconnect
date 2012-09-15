from django import forms


class SearchForm(forms.Form):
    SEARCH_TYPE_CHOICES = (
        ('all', 'All'),
        ('collection', 'Collections only'),
        ('listing', 'Listings only'),
    )

    query = forms.CharField(max_length=200, required=True)
    search_type = forms.ChoiceField(choices=SEARCH_TYPE_CHOICES, required=True)
