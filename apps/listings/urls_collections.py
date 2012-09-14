from django.conf.urls import patterns, include, url

urlpatterns = patterns('listings.views',
    url(r'^add/$', 'add_collection', name='add'),
    url(r'^like/(?P<collection_id>[\d]+)/$', 'like_collection', name='like'),
    url(r'^add-listings/(?P<collection_id>[\d]+)/$', 'add_collection_listings', name='add_listings'),
    url(r'^(?P<collection_id>[\d]+)/$', 'view_collection', name='view'),
    url(r'^$', 'view_collections', name='index'),
)
