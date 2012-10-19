from django.conf.urls import patterns, include, url

urlpatterns = patterns('payments.views',
    url(r'^pdt/$', 'pdt', name='pdt'),
    url(r'^make-payment/(?P<payment_id>[\d]+)/$', 'make_payment', name='make_payment'),
    url(r'^$', 'index', name='index'),
)
