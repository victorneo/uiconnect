from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from categories.models import Category
from .forms import (AddListingForm, AddImageForm,
        AddCollectionForm, AddCollectionListingsForm)
from .models import Listing, ListingImage, Collection


def index(request):
    categories = Category.objects.all()
    for c in categories:
        c.featured_listings = c.listings.filter(is_featured=True).all()

    return render(request, 'index.html', {
        'categories': categories,
    })


def view(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'listings/view.html', {
        'listing': listing,
    })


@login_required
def dashboard(request):
    listings = Listing.objects.filter(user=request.user).all()
    collections = Collection.objects.filter(user=request.user).all()
    return render(request, 'listings/dashboard.html', {
        'listings': listings,
        'collections': collections,
    })


@login_required
def add(request):
    form = AddListingForm(request.POST or None)

    if form.is_valid():
        listing = form.save(commit=False)
        listing.user = request.user
        listing.save()
        for c in form.cleaned_data['categories']:
            listing.categories.add(c)

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
def update(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if listing.user != request.user:
        return redirect(reverse('listings:view', kwargs={'listing_id': listing_id}))

    return render(request, 'listings/update.html', {
        'listing': listing,
    })


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


def view_collections(request):
    col_type = request.GET.get('type', None)
    qs = Collection.objects

    if col_type =='new':
        qs.order_by('-created_at')
    else:
        qs.filter(is_featured=True)

    collections = qs.all()[:10]

    return render(request, 'collections/collections.html', {
        'type': col_type,
        'collections': collections,
    })


def view_collection(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)

    return render(request, 'collections/view.html', {
        'collection': collection,
    })



@login_required
def add_collection_listings(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    form = AddCollectionListingsForm(request.POST or None, instance=collection)

    if form.is_valid():
        existing_listings = set(collection.listings.all())
        curr_listings = set(form.cleaned_data['listings'])

        # delete invalid listings
        for l in existing_listings.difference(curr_listings):
            collection.listings.remove(l)

        # add new listings
        for l in curr_listings.difference(existing_listings):
            collection.listings.add(l)

        collection.save()
        form = AddCollectionListingsForm(instance=collection)

        messages.success(request, u'Changes saved!')

    return render(request, 'collections/add_listings.html', {
        'form': form,
    })


@login_required
def add_collection(request):
    form = AddCollectionForm(request.POST or None)

    if form.is_valid():
        collection = form.save(commit=False)
        collection.user = request.user
        collection.save()

        messages.success(request, u'Collection added. Add your listings to it!')
        return redirect(reverse('collections:add_listings', kwargs={
            'collection_id': collection.id,
        }))

    return render(request, 'collections/add.html', {
        'form': form,
    })
