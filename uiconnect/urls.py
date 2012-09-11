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
    url(r'^categories/', include('categories.urls', namespace='categories')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^listings/', include('listings.urls', namespace='listings')),
    url(r'^collections/', include('listings.urls_collections', namespace='collections')),
    url(r'^dashboard/$', 'listings.views.dashboard', name='dashboard'),
    url(r'^$', 'listings.views.index', name='index'),
)
