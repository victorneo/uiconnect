from django.db.models import Q
from django.shortcuts import render
from listings.models import Listing, Collection
from .forms import SearchForm


def results(request):
    form = SearchForm(request.POST)
    listings = None
    collections = None
    query = None

    if form.is_valid():
        search_type = form.cleaned_data['search_type']
        query = form.cleaned_data['query']

        if search_type == 'all' or search_type == 'listing':
            listings = Listing.objects.filter(Q(name__contains=query) | Q(description__contains=query)).all()

        if search_type == 'all' or search_type == 'collection':
            collections = Collection.objects.filter(Q(name__contains=query) | Q(description__contains=query)).all()


    return render(request, 'search/results.html', {
        'form': form,
        'listings': listings,
        'collections': collections,
        'query': query,
    })

