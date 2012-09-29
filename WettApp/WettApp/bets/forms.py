# -*- coding: utf-8 -*-

from django import forms

from WettApp.bets.models import Bet, BetScore


class NewBetForm(forms.ModelForm):
    opponent = forms.ModelChoiceField(queryset=None, empty_label=None)

    class Meta:
        model = Bet
        fields = ('title', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(NewBetForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['opponent'].queryset = (self.user.get_profile()
                                                .buddies())

    def save(self):
        new_bet = super(NewBetForm, self).save()
        participants = (self.user, self.cleaned_data['opponent'])
        new_bet.participants.add(*participants)
        for user in participants:
            BetScore(user=user, bet=new_bet).save()
