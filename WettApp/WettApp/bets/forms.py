# -*- coding: utf-8 -*-

from django import forms


class NewBetForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=500, widget=forms.Textarea)
    opponent = forms.ModelChoiceField(queryset=None, empty_label=None)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(NewBetForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['opponent'].queryset = user.get_profile().buddies()
