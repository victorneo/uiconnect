from django.conf.urls import patterns, include, url

urlpatterns = patterns('listings.views',
    url(r'^$', 'index', name='index'),
    url(r'^add/$', 'add', name='add'),
    url(r'^manage-images/(?P<listing_id>[\d]+)/$', 'manage_images', name='manage_images'),
    url(r'^delete-image/(?P<listing_id>[\d]+)/(?P<image_id>[\d]+)/$', 'delete_image', name='delete_image'),
)
