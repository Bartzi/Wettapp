# -*- coding: utf-8 -*-

from django import forms
from WettApp.users.models import UserProfile
from WettApp.bets.models import Bet


class NewBetForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=500, widget=forms.Textarea)
    opponent = forms.ModelChoiceField(Bet.objects.all())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(NewBetForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['opponent'].queryset = UserProfile.objects.filter(buddies__username__exact=user.username)
