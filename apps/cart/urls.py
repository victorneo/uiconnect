from django.conf.urls import patterns, include, url

urlpatterns = patterns('cart.views',
    url(r'^add/(?P<listing_id>[\d]+)/$', 'add', name='add'),
    url(r'^remove/(?P<listing_id>[\d]+)/$', 'remove', name='remove'),
    url(r'^checkout/$', 'checkout', name='checkout'),
    url(r'^$', 'view', name='view'),
)
