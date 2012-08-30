from django.conf.urls import patterns, include, url

urlpatterns = patterns('listings.views',
    url(r'^$', 'index', name='index'),
)
