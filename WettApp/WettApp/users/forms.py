# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from WettApp.users.models import UserProfile


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        """ Make a nicer label for password confirmation field. """
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password2'].label = 'Confirm Password'

    def save(self, *args, **kwargs):
        self.instance.email = self.cleaned_data['email']
        self.instance.is_active = False
        super(RegisterForm, self).save(*args, **kwargs)
        UserProfile(user=self.instance).save()
        return self.instance


class EditUserForm(forms.ModelForm):
    password1 = forms.CharField(required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(required=False, widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError("Passwords are not identical.")
        return password2

    def save(self, *args, **kwargs):
        password = self.cleaned_data['password1']
        if password:
            self.instance.set_password(password)
        return super(EditUserForm, self).save(*args, **kwargs)

    class Meta:
        model = User
        fields = ('username', 'is_active', 'is_superuser', 'email', 'password1', 'password2')


class RestrictedEditUserForm(EditUserForm):
    old_password = forms.CharField(required=False, widget=forms.PasswordInput)

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if old_password and not self.instance.check_password(old_password):
            raise forms.ValidationError("Wrong password.")
        return old_password

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
