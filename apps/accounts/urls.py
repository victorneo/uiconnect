from django.conf.urls import patterns, include, url

urlpatterns = patterns('accounts.views',
    url(r'^login/', 'login', name='login'),
    url(r'^forgot-password/', 'forgot_password', name='forgot_password'),
    url(r'^profile/', 'profile', name='profile'),
    url(r'^logout/', 'logout', name='logout'),
    url(r'^register/', 'register', name='register'),
)
