# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models


class Bet(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    start_date = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User)

    def participant_score(self, participant):
        return self.bet_scores.get(user=participant)

    def __unicode__(self):
        return self.title


class BetScore(models.Model):
    score = models.IntegerField(default=0)
    user = models.ForeignKey(User, related_name='bet_scores')
    bet = models.ForeignKey(Bet, related_name='bet_scores')

    def __unicode__(self):
        return unicode(self.score)


class BetScoreHistoryEntry(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='bet_histories')
    bet = models.ForeignKey(Bet, related_name='bet_histories')

    def __unicode__(self):
        return "date: " + unicode(self.date)

    def has_been_changed_recently(self):
        pass
