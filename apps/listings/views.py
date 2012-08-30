from django.shortcuts import render, redirect
from .models import Listing, ListingImage


def index(request):
    return render(request, 'index.html', {
        'listings': Listing.objects.all(),
    })
