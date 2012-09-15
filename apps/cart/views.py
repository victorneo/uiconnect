from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
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
