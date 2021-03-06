import json
import urllib
from datetime import datetime
from decimal import Decimal
from operator import attrgetter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from categories.models import Category
from comments.forms import CommentForm
from .forms import (ListingForm, AddImageForm,
                    CollectionForm, AddCollectionListingsForm,
                    CaptionForm)
from .models import Listing, ListingImage, Collection


def index(request):
    categories = Category.objects.all()
    for c in categories:
        c.featured_listings = c.listings.filter(is_featured=True).all()

    return render(request, 'index.html', {
        'categories': categories,
    })


def discover(request):
    listings = Listing.objects.order_by('-id').all()[:20]
    categories = Category.objects.all()

    for c in categories:
        c.display_listings = c.listings.order_by('-id').all()

    request.session['discover_time'] = datetime.now()

    return render(request, 'listings/discover.html', {
        'listings': listings,
        'categories': categories,
    })


def discover_items(request):
    category_id = request.GET.get('category_id', 0)
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        category = None

    if category:
        listings = category.listings.order_by('-id')
    else:
        listings = Listing.objects.order_by('-id')

    listings = listings.annotate(img_count=Count('images')).filter(img_count__gt=0).all()[:20]

    items = [{'thumbnail': l.images.all()[0].image.url, 'url': reverse('listings:view', kwargs={'listing_id': l.id})} for l in listings if l.images.count() > 0]
    data = {'items': items}

    request.session['discover_time'] = datetime.now()

    return HttpResponse(json.JSONEncoder().encode(data),
                        content_type='application/json')


def discover_new_items(request):
    category_id = request.GET.get('category_id', 0)
    prev_time = request.session['discover_time']

    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        category = None

    if category:
        listings = category.listings.order_by('-id')
    else:
        listings = Listing.objects.order_by('-id')

    listings = listings.annotate(img_count=Count('images')).filter(created_at__gt=prev_time,img_count__gt=0).all()

    items = [{'thumbnail': l.images.all()[0].image.url, 'url': reverse('listings:view', kwargs={'listing_id': l.id})} for l in listings if l.images.count() > 0]
    data = {'items': items}

    request.session['discover_time'] = datetime.now()

    return HttpResponse(json.JSONEncoder().encode(data),
                        content_type='application/json')


def categories(request):
    categories = Category.objects.all()
    for c in categories:
        c.display_listings = c.listings.annotate(num_likes=Count('likes'))\
            .order_by('-num_likes')\
            .filter(quantity__gte=1)\
            .all()[:4]

    return render(request, 'listings/categories.html', {
        'categories': categories,
    })


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    sort_type = request.GET.get('sort_type', None)

    if sort_type:
        category.display_listings = category.listings.order_by('-id').filter(quantity__gte=1).all()
    else:
        category.display_listings = category.listings\
            .annotate(num_likes=Count('likes'))\
            .order_by('-num_likes')\
            .filter(quantity__gte=1)\
            .all()

    return render(request, 'listings/category.html', {
        'category': category,
        'sort_type': sort_type,
    })


def view(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    form = CommentForm(request.POST or None)
    commented = None

    comments = listing.comments.order_by('created_at').all()

    if form.is_valid() and request.user.is_authenticated():
        comment = form.save(commit=False)
        comment.content_object = listing
        comment.user = request.user
        comment.save()
        commented = comment.id

    return render(request, 'listings/view.html', {
        'listing': listing,
        'comments': comments,
        'commented': commented,
    })


@login_required
def dashboard(request):
    updates = []
    following_users = request.user.get_profile().following.all()
    if following_users.count() > 0:
        updates = list(Listing.objects.filter(user__profile__in=following_users)\
                        .order_by('-created_at').all()[:20])
        updates.extend(list(Collection.objects.filter(user__profile__in=following_users).order_by('-created_at').all()[:20]))

        updates = sorted(updates, key=attrgetter('created_at'), reverse=True)

    return render(request, 'listings/dashboard.html', {
        'updates': updates,
    })


@login_required
def items_and_collections(request):
    listings = Listing.objects.filter(user=request.user).annotate(num_likes=Count('likes')).order_by('-num_likes').all()
    collections = Collection.objects.filter(user=request.user).all()

    return render(request, 'listings/items_and_collections.html', {
        'listings': listings,
        'collections': collections,
    })


@login_required
def add(request):
    form = ListingForm(request.POST or None)

    if form.is_valid():
        listing = form.save(commit=False)
        listing.user = request.user
        listing.save()
        for c in form.cleaned_data['categories']:
            listing.categories.add(c)

        listing.save()
        messages.success(request, u'Your item has been created. Upload some images!')
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
    messages.success(request, u'Item has been deleted.')

    return redirect(reverse('items_and_collections'))


@login_required
def update(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if listing.user != request.user:
        return redirect(reverse('listings:view', kwargs={'listing_id': listing_id}))

    form = ListingForm(request.POST or None, instance=listing, submit_name=u'Update')

    if form.is_valid():
        listing = form.save()
        messages.success(request, u'Item updated.')
        return redirect(reverse('listings:view', kwargs={'listing_id': listing.id}))

    return render(request, 'listings/update.html', {
        'listing': listing,
        'form': form,
    })


@login_required
def like(request, listing_id):
    data = {'success': True}
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        data['success'] = False
    else:
        if listing in request.user.liked_listings.all():
            listing.likes.remove(request.user)
        else:
            listing.likes.add(request.user)

        listing.save()

    return HttpResponse(json.JSONEncoder().encode(data),
                        content_type='application/json')


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
            pass
        else:
            img.delete()

    return redirect(reverse('listings:manage_images', kwargs={'listing_id': listing_id}))


@csrf_exempt
@login_required
def update_image_caption(request, listing_id, image_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    data = {'success': False}
    try:
        img = listing.images.get(id=image_id)
    except ListingImage.DoesNotExist:
        img = None

    if img is None or listing.user != request.user:
        return redirect(reverse('items_and_collections'))

    form = CaptionForm(request.POST, instance=img)

    if form.is_valid():
        form.save()
        data['success'] = True

    return HttpResponse(json.JSONEncoder().encode(data),
                        content_type='application/json')


def view_collections(request):
    col_type = request.GET.get('type', None)
    qs = Collection.objects

    if col_type =='new':
        qs = qs.order_by('-created_at')
    else:
        qs = qs.filter(is_featured=True)

    collections = qs.all()

    return render(request, 'collections/collections.html', {
        'type': col_type,
        'collections': collections,
    })


def view_collection(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    form = CommentForm(request.POST or None)
    commented = None

    if form.is_valid() and request.user.is_authenticated():
        comment = form.save(commit=False)
        comment.content_object = collection
        comment.user = request.user
        comment.save()
        commented = comment.id

    return render(request, 'collections/view.html', {
        'collection': collection,
        'commented': commented,
    })


@login_required
def like_collection(request, collection_id):
    data = {'success':  True}
    try:
        collection = Collection.objects.get(pk=collection_id)
    except Collection.DoesNotExist:
        data['success'] = False
    else:
        if collection in request.user.liked_collections.all():
            collection.likes.remove(request.user)
        else:
            collection.likes.add(request.user)

        collection.save()

    return HttpResponse(json.JSONEncoder().encode(data),
                        content_type='application/json')

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
        return redirect(reverse('collections:view', kwargs={'collection_id': collection.id}))

    return render(request, 'collections/add_listings.html', {
        'form': form,
    })


@login_required
def add_collection(request):
    form = CollectionForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        collection = form.save(commit=False)
        collection.user = request.user
        collection.save()

        messages.success(request, u'Collection added. Add your items to it!')
        return redirect(reverse('collections:add_listings', kwargs={
            'collection_id': collection.id,
        }))

    return render(request, 'collections/add.html', {
        'form': form,
    })


@login_required
def update_collection(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)

    if collection.user != request.user:
        return redirect(reverse('collections:view', kwargs={'collection_id': collection_id}))

    form = CollectionForm(request.POST or None, request.FILES or None, instance=collection, submit_name=u'Update')

    if form.is_valid():
        collection = form.save()

        messages.success(request, u'Collection Updated.')
        return redirect(reverse('collections:view', kwargs={
            'collection_id': collection.id,
        }))

    return render(request, 'collections/update.html', {
        'form': form,
    })


@login_required
def delete_collection(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)

    if collection.user != request.user:
        return redirect(reverse('collections:view', kwargs={'collection_id': collection_id}))

    collection.delete()
    messages.success(request, u'Collection has been deleted.')

    return redirect(reverse('items_and_collections'))


@csrf_exempt
def aviary_post(request, image_id):
    url = request.POST.get('url', None)
    image = get_object_or_404(ListingImage, pk=image_id)

    if not url:
        return HttpResponse(status_code=500)

    try:
        img = urllib.urlretrieve(url)
        f = File(open(img[0], 'rb'))
        image.image = f
        image.save()
    except urllib.ContentTooShortError:
        print('Unable to download file %s for image id %s' % (url, image_id))
        return HttpResponse(status_code=500)
    except Exception as e:
        print e
        print img
        print image

    return HttpResponse("Ok.", content_type="text/plain")
