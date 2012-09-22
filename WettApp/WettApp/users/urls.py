from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns('WettApp.users.views',
    url(ur'^login/$', login, {'template_name': 'users/login.html'},
        name='login'),
    url(ur'^logout/$', logout, {'next_page': reverse_lazy('login')},
        name='logout'),
)