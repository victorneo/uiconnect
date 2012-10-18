from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from listings.models import Listing
from payments.models import Discount, Payment, PaymentItem
from .forms import AddItemForm, PaymentForm
from .models import Cart, Item


@login_required
def view(request):
    cart = request.user.cart
    initial = {'address': request.user.get_profile().address}
    if request.GET.get('edit', None):
        try:
            payment = request.user.payments.get(is_paid=False)
            initial['address'] = payment.address
        except:
            request.user.payments.filter(is_paid=False).all().delete()

        try:
            discount = payment.discount
            initial['discount_code'] = discount.code
        except Discount.DoesNotExist:
            pass

    form = CartForm(request.POST or None, cancel_url=reverse('listings:categories'), initial=initial)

    if form.is_valid():
        cart = form.save()

        # only save address if it is empty
        if not request.user.get_profile().address:
            request.user.get_profile().address = cart.address
            request.user.get_profile().save()

        if form.cleaned_data['discount_code']:
            try:
                discount = Discount.objects.get(
                    code=form.cleaned_data['discount_code'],
                    user=request.user)
            except (Discount.DoesNotExist, Payment.DoesNotExist) as e:
                discount = None

            if not discount:
                messages.error(request, u'Invalid discount code given. No discount applied.')
            else:
                cart.discount_code = discount.code

        return redirect(reverse('cart:checkout'))

    return render(request, 'cart/view.html', {
        'cart': cart,
        'form': form,
    })


@login_required
def checkout(request):
    cart = request.user.cart
    amount = cart.total

    if cart.discount_code:
        try:
            discount = Discount.objects.get(
                code=cart.discount_code,
                user=request.user,
                payment=None)
        except (Discount.DoesNotExist, Payment.DoesNotExist) as e:
            discount = None

    payment = request.user.payments.get(is_paid=False)

    if request.method == 'POST' and request.POST.get('confirm', None):
        payment = Payment(user=request.user, address=cart.address)
        payment.save()

        if discount:
            discount.payment = payment
            discount.save()

        # move listings over to payment and clear the shopping cart
        for i in cart.items.all():
            PaymentItem.objects.create(
                    listing=i.listing,
                    quantity=i.quantity,
                    payment=payment)

            i.listing.quantity -= i.quantity
            i.listing.save()

        payment.save()
        cart.clear()

        # redirect to payment
        return redirect(reverse('payments:make_payment',
                                 kwargs={'payment_id': payment.id}))

    return render(request, 'cart/checkout.html', {
        'cart': cart,
        'payment': payment,
        'discount': discount,
        'amount': amount,
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
        messages.success(request, u'removed item from cart.')

    return redirect(reverse('cart:view'))


@login_required
def empty(request):
    request.user.cart.clear()
    return redirect(reverse('cart:view'))
