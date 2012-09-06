from decimal import Decimal
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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


@login_required
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


@login_required
def delete(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if listing.user != request.user:
        return redirect(reverse('listings:view', kwargs={'listing_id': listing_id}))

    listing.delete()
    messages.success(request, u'Listing has been deleted.')

    return redirect(reverse('index'))


@login_required
@csrf_exempt
def update(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if listing.user != request.user:
        return redirect(reverse('listings:view', kwargs={'listing_id': listing_id}))

    param = request.POST['id']
    value = request.POST['value']

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


@login_required
def manage_images(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if listing.user != request.user:
        return redirect(reverse('listings:view', kwargs={'listing_id': listing_id}))

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


@login_required
def delete_image(request, listing_id, image_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if listing.user == request.user:
        try:
            img = listing.images.get(id=image_id)
        except ListingImage.DoesNotExist as e:
            print('Attmpted to delete non existant image')
            print e
        else:
            img.delete()

    return redirect(reverse('listings:manage_images', kwargs={'listing_id': listing_id}))
