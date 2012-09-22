# -*- coding: utf-8 -*-

from django.contrib.auth import views as authviews

from WettApp.users.forms import LoginForm


def login(request):
    if request.method == 'POST' and not request.POST.get('remember_me', None):
        request.session.set_expiry(0)
    return authviews.login(request, template_name='users/login.html',
                           authentication_form=LoginForm)
