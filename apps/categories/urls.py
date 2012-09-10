from django.conf.urls import patterns, include, url

urlpatterns = patterns('categories.views',
    url(r'^list/$', 'list', name='list'),
)

