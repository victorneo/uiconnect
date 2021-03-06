from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'uiconnect.views.home', name='home'),
    # url(r'^uiconnect/', include('uiconnect.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^items/', include('listings.urls', namespace='listings')),
    url(r'^collections/', include('listings.urls_collections', namespace='collections')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^rewards/', include('rewards.urls', namespace='rewards')),
    url(r'^payments/', include('payments.urls', namespace='payments')),
    url(r'^dashboard/$', 'listings.views.dashboard', name='dashboard'),
    url(r'^my-items-and-collections/$', 'listings.views.items_and_collections', name='items_and_collections'),
    url(r'^$', 'listings.views.index', name='index'),
)
