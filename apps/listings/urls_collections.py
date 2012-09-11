from django.conf.urls import patterns, include, url

urlpatterns = patterns('listings.views',
    url(r'^add/$', 'add_collection', name='add_collection'),
    url(r'^$', 'view_collections', name='index'),
)
