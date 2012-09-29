from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render
from paypal.standard.pdt.models import PayPalPDT
from paypal.standard.pdt.forms import PayPalPDTForm
from .models import Payment


@login_required
def index(request):
    payments = request.user.payments.all()

    return render(request, 'payments/index.html', {
        'payments': payments,
    })


@login_required
def pdt(request):
    """Payment data transfer implementation: http://tinyurl.com/c9jjmw"""
    context = {}
    pdt_obj = None
    txn_id = request.GET.get('tx')
    failed = False
    item_check_callable=None
    if txn_id is not None:
        # If an existing transaction with the id tx exists: use it
        try:
            pdt_obj = PayPalPDT.objects.get(txn_id=txn_id)
        except PayPalPDT.DoesNotExist:
            # This is a new transaction so we continue processing PDT request
            pass

        if pdt_obj is None:
            form = PayPalPDTForm(request.GET)
            if form.is_valid():
                try:
                    pdt_obj = form.save(commit=False)
                except Exception, e:
                    error = repr(e)
                    failed = True
            else:
                error = form.errors
                failed = True

            if failed:
                pdt_obj = PayPalPDT()
                pdt_obj.set_flag("Invalid form. %s" % error)

            pdt_obj.initialize(request)

            if not failed:
                # The PDT object gets saved during verify
                pdt_obj.verify(item_check_callable)

                if pdt_obj.id:
                    payment = request.user.payments.get(is_paid=False)
                    payment.is_paid = True
                    payment.pdt = pdt_obj
                    payment.save()

                    # clear shopping cart
                    request.user.cart.clear()

                    # calculate points earned
                    payment.allocate_points()
                    context['payment'] = payment

    else:
        pass # we ignore any PDT requests that don't have a transaction id

    context.update({"failed":failed, "pdt_obj":pdt_obj})
    return render(request, 'payments/success.html', context)
