from django.conf.urls import patterns, include, url

urlpatterns = patterns('listings.views',
    url(r'^$', 'index', name='index'),
    url(r'^add/$', 'add', name='add'),
    url(r'^manage-images/(?P<listing_id>[\d]+)/$', 'manage_images', name='manage_images'),
)
