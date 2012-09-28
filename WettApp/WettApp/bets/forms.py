# -*- coding: utf-8 -*-

from django import forms
from WettApp.bets.models import Bet, BetScore
from django.utils.timezone import utc
import datetime

#class NewBetForm(forms.Form):
#    title = forms.CharField(max_length=100)
#    description = forms.CharField(max_length=500, widget=forms.Textarea)
#    opponent = forms.ModelChoiceField(queryset=None, empty_label=None)
#
#    def __init__(self, *args, **kwargs):
#        user = kwargs.pop('user', None)
#        super(NewBetForm, self).__init__(*args, **kwargs)
#        if user:
#            self.fields['opponent'].queryset = user.get_profile().buddies()


class NewBetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ('title', 'description', 'participants')
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
           # 'participants': forms.Select()
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(NewBetForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['participants'].queryset = user.get_profile().buddies()
        else:
            self.fields['participants'].queryset = None

    def save(self, user):
        current_bet = super(NewBetForm, self).save(commit=False)
        current_bet.start_date = datetime.datetime.utcnow().replace(tzinfo=utc)
        current_bet.save()
        current_bet.participants.add(user)
        for opponent in self.cleaned_data['participants']:
            current_bet.participants.add(opponent)
            bet_score = BetScore()
            bet_score.score = 0
            bet_score.user = opponent
            bet_score.bet = current_bet
            bet_score.save()
        current_bet.save()
        bet_score = BetScore()
        bet_score.score = 0
        bet_score.user = user
        bet_score.bet = current_bet
        bet_score.save()
