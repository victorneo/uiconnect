from django.conf.urls import patterns, include, url

urlpatterns = patterns('listings.views',
    url(r'^add/$', 'add', name='add'),
    url(r'^like/(?P<listing_id>[\d]+)/$', 'like', name='like'),
    url(r'^update/(?P<listing_id>[\d]+)/$', 'update', name='update'),
    url(r'^delete/(?P<listing_id>[\d]+)/$', 'delete', name='delete'),
    url(r'^(?P<listing_id>[\d]+)/$', 'view', name='view'),
    url(r'^manage-images/(?P<listing_id>[\d]+)/$', 'manage_images', name='manage_images'),
    url(r'^delete-image/(?P<listing_id>[\d]+)/(?P<image_id>[\d]+)/$', 'delete_image', name='delete_image'),
    url(r'^(?P<listing_id>[\d]+)/$', 'view', name='view'),
    url(r'^$', 'index', name='index'),
)
