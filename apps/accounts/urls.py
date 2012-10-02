from django.conf.urls import patterns, include, url

urlpatterns = patterns('accounts.views',
    url(r'^login/', 'login', name='login'),
    url(r'^forgot-password/', 'forgot_password', name='forgot_password'),
    url(r'^facebook-login/', 'facebook_login', name='facebook_login'),
    url(r'^persona-login/', 'persona_login', name='persona_login'),
    url(r'^profile/', 'update_profile', name='profile'),
    url(r'^logout/', 'logout', name='logout'),
    url(r'^register/', 'register', name='register'),
    url(r'^following/', 'following', name='following'),
    url(r'^follow/(?P<user_id>[\d]+)/$', 'follow', name='follow'),
    url(r'^unfollow/(?P<user_id>[\d]+)/$', 'unfollow', name='unfollow'),
    url(r'^(?P<user_id>[\d]+)/?', 'view_profile', name='view_profile'),
)
