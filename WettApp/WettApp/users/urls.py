from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login

urlpatterns = patterns('WettApp.users.views',
    url(ur'^login/$', login, {'template_name': 'users/login.html'},
        name='login'),
)