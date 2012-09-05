from decimal import Decimal
import json
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .forms import AddListingForm, AddImageForm
from .models import Listing, ListingImage


def index(request):
    return render(request, 'index.html', {
        'listings': Listing.objects.all(),
    })


def view(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'listings/view.html', {
        'listing': listing,
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


def delete(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        if request.user != listing.user:
            listing = None
    except Listing.DoesNotExist:
        listing = None

    if listing is None:
        return redirect(reverse('listings:index'))

    for img in listing.images.all():
        img.formatted_image.delete()
        img.thumbnail.delete()

    listing.delete()
    messages.success(request, u'Listing has been deleted.')

    return redirect(reverse('index'))


@csrf_exempt
def update(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        if request.user != listing.user:
            listing = None
    except Listing.DoesNotExist:
        listing = None

    if listing is None:
        return redirect(reverse('listings:index'))

    param = request.POST['id']
    value = request.POST['value']

    print param, value

    if param == 'listing_name':
        listing.name = value
    elif param == 'listing_description':
        listing.description = value
    else:
        try:
            listing.price = Decimal(value)
        except Exception as e:
            print e

    try:
        listing.save()
    except Exception as e:
        print e

    return HttpResponse(value)


def manage_images(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        if request.user != listing.user:
            listing = None
    except Listing.DoesNotExist:
        listing = None

    if listing is None:
        return redirect(reverse('listings:index'))

    form = AddImageForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        img = ListingImage(
            listing=listing,
            image=form.cleaned_data['img'],
            caption=form.cleaned_data['caption'],
        )
        img.save()
        messages.success(request, u'Image uploaded!')
        return redirect(reverse('listings:manage_images', kwargs={'listing_id': listing_id}))

    return render(request, 'listings/images.html', {
        'listing': listing,
    })


def delete_image(request, listing_id, image_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        if request.user != listing.user:
            listing = None

        img = listing.images.get(id=image_id)
    except Listing.DoesNotExist:
        listing = None
    except ListingImage.DoesNotExist:
        img = None

    if listing is None or img is None:
        return redirect(reverse('index'))

    img.thumbnail.delete()
    img.formatted_image.delete()
    img.delete()

    return redirect(reverse('listings:manage_images', kwargs={'listing_id': listing_id}))
