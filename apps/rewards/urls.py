from django.conf.urls import patterns, include, url

urlpatterns = patterns('rewards.views',
    url(r'^$', 'index', name='index'),
)
