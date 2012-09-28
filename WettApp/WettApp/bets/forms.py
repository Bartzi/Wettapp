# -*- coding: utf-8 -*-

from django import forms
from WettApp.bets.models import Bet, BetScore
from django.utils.timezone import utc
import datetime


class NewBetForm(forms.ModelForm):
    opponent = forms.ModelChoiceField(queryset=None, empty_label=None)

    class Meta:
        model = Bet
        fields = ('title', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(NewBetForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['opponent'].queryset = user.get_profile().buddies()
        else:
            self.fields['opponent'].queryset = None

    def save(self, user):
        current_bet = super(NewBetForm, self).save(commit=False)
        current_bet.start_date = datetime.datetime.utcnow().replace(tzinfo=utc)
        current_bet.save()
        current_bet.participants.add(user)
        opponent = self.cleaned_data['opponent']
        current_bet.participants.add(opponent)
        current_bet.save()
        bet_score = BetScore()
        bet_score.score = 0
        bet_score.user = user
        bet_score.bet = current_bet
        bet_score.save()
        bet_score = BetScore()
        bet_score.score = 0
        bet_score.user = opponent
        bet_score.bet = current_bet
        bet_score.save()
