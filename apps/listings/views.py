from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import AddListingForm, ListingImageForm
from .models import Listing, ListingImage


def index(request):
    return render(request, 'index.html', {
        'listings': Listing.objects.all(),
    })


def add(request):
    form = AddListingForm(request.POST or None)

    if form.is_valid():
        listing = form.save(commit=False)
        listing.user = request.user
        listing.save()
        messages.success(request, u'Your listing has been created. Upload some images!')
        return redirect(reverse('listings:manage_images', kwargs={'listing_id': listing.id}))

    return render(request, 'listings/add.html', {
        'form': form,
    })


def manage_images(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        if request.user != listing.user:
            listing = None
    except Listing.DoesNotExist:
        listing = None

    if listing is None:
        return redirect('listings:index')

    initial = {}
    count = 1
    for img in listing.images.all()[:3]:
        initial['image%d' % count] = img
        count += 1

    form = ListingImageForm(request.POST or None, request.FILES or None, initial=initial)

    if form.is_valid():
        data = form.cleaned_data

        message.success(request, u'Images uploaded successfully.')
        return redirect(reverse('listings:manage_images', kwargs={'listing_id': listing.id}))

    return render(request, 'listings/images.html', {
        'form': form,
        'listing': listing,
    })
