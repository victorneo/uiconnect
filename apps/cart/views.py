from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from listings.models import Listing
from .forms import AddItemForm, PaymentForm
from .models import Cart, Item


@login_required
def view(request):
    cart = request.user.cart
    form = PaymentForm(request.POST or None, cancel_url=reverse('listings:categories'))

    if form.is_valid():
        # delete any unpaid payments
        request.user.payments.filter(is_paid=False).all().delete()

        payment = form.save(commit=False)
        payment.user = request.user
        payment.save()

        for l in cart.items.all():
            payment.listings.add(l.listing)

        payment.save()

        return redirect(reverse('cart:checkout'))

    return render(request, 'cart/view.html', {
        'cart': cart,
        'form': form,
    })


@login_required
def checkout(request):
    cart = request.user.cart
    payment = request.user.payments.get(is_paid=False)
    domain = Site.objects.all()[0].domain

    paypal_dict = {
        'business': 'seller_1347808967_biz@gmail.com',
        'amount': str(cart.total),
        "invoice": "%d" % payment.id,
        'item_name': 'UIConnect items',
        'return_url': 'http://%s/payments/pdt' % domain,
    }

    paypal_form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'cart/checkout.html', {
        'cart': cart,
        'payment': payment,
        'paypal_form': paypal_form,
    })


@login_required
def add(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    cart = request.user.cart

    if listing.user == request.user:
        return redirect(reverse('listings:view', kwargs={'listing_id': listing_id}))

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
