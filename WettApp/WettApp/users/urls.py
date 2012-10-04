# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.auth.views import logout
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns('WettApp.users.views',
    url(ur'^login/$', 'login', name='login'),
    url(ur'^logout/$', logout, {'next_page': reverse_lazy('login')},
        name='logout'),
    url(ur'^buddies/$', 'buddy_list', name='buddy-list'),
    url(ur'^edit/(?P<user_id>\d+)/$', 'edit_user', name='edit-user'),
)
