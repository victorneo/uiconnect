from django.conf.urls import patterns, include, url

urlpatterns = patterns('payments.views',
    url(r'^pdt/$', 'pdt', name='pdt'),
    url(r'^$', 'index', name='index'),
)
