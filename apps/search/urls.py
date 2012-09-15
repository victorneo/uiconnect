from django.conf.urls import patterns, include, url

urlpatterns = patterns('search.views',
    url(r'^results/$', 'results', name='results'),
)

