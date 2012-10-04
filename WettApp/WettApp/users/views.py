# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import views as authviews
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

from WettApp.users.forms import LoginForm, EditUserForm, RestrictedEditUserForm


def login(request):
    if request.method == 'POST' and not request.POST.get('remember_me', None):
        request.session.set_expiry(0)
    return authviews.login(request, template_name='users/login.html',
                           authentication_form=LoginForm)


@login_required
def buddy_list(request):
    buddies = request.user.get_profile().buddies()
    return render(request, 'users/buddy_list.html', {'buddies': buddies})


@login_required
def edit_user(request, user_id):
    if not request.user.is_superuser:
        if request.user.pk != int(user_id):
            raise PermissionDenied('No permission to edit this user.')
        form_class = RestrictedEditUserForm
    else:
        form_class = EditUserForm
    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        form = form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been saved.")
            return redirect('index-bets')
    else:
        form = form_class(instance=user)
    return render(request, 'users/edit_user.html',
                  {'user_': user, 'form': form})
