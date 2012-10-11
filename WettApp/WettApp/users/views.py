# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import views as authviews
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from WettApp.users.forms import LoginForm, RegisterForm, \
    EditUserForm, RestrictedEditUserForm


ACTIVATION_MESSAGE = """
Welcome to WettApp!\n
Before you can login, your must activate your account.\n
To do so visit the following link:
http://{0}/users/activate/{1}/{2}
"""


def login(request):
    if request.method == 'POST' and not request.POST.get('remember_me', None):
        request.session.set_expiry(0)
    return authviews.login(request, template_name='users/login.html',
                           authentication_form=LoginForm)


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_mail('WettApp Account Activation',
                ACTIVATION_MESSAGE.format(request.get_host(), user.pk,
                                          user.get_profile().activation_key),
                'noreply@wettapp.de', [user.email])
            messages.success(request, 'Registration successfull.')
            messages.info(request, 'Check your emails to activate the \
                                    account.')
            return redirect('root')
    else:
        form = RegisterForm()
    return render(request, 'users/register_user.html', {'form': form})


def activate_user(request, user_id, key):
    user = User.objects.get(pk=user_id)
    if user.is_active:
        messages.error(request, 'Account has already been activated.')
    elif user.get_profile().activation_key == key:
        user.is_active = True
        user.save()
        messages.success(request, 'Account has been activated.')
    else:
        messages.success(request, 'Account could not be activated.')
    return redirect('root')


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
