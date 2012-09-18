from django.conf.urls import patterns, include, url

urlpatterns = patterns('rewards.views',
    url(r'^$', 'index', name='index'),
    url(r'^redeem/(?P<reward_id>[\d]+)/$', 'redeem', name='redeem'),
)
