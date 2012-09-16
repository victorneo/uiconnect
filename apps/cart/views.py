from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from listings.models import Listing
from .forms import AddItemForm
from .models import Cart, Item


@login_required
def view(request):
    try:
        cart = request.user.cart
    except Cart.DoesNotExist:
        cart = Cart(user=request.user)
        cart.save()

    return render(request, 'cart/view.html', {
        'cart': cart,
    })


@login_required
def add(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    cart = request.user.cart

    try:
        item = cart.items.get(listing=listing)
    except Item.DoesNotExist:
        item = Item(cart=cart, listing=listing)
        item.save()

    form = AddItemForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        messages.success(request, u'Added to your shopping cart.')

    return redirect(reverse('listings:view', kwargs={'listing_id': listing.id}))


@login_required
def remove(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    cart = request.user.cart

    try:
        item = cart.items.get(listing=listing)
    except Item.DoesNotExist:
        pass
    else:
        item.delete()
        messages.success(request, u'Removed item from cart.')

    return redirect(reverse('cart:view'))
