# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Bet(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    start_date = models.DateTimeField('start Date')
    participants = models.ManyToManyField(User)

    def participant_score(self, participant):
        return self.bet_scores.get(user=participant)

    def __unicode__(self):
        return self.title


class BetScore(models.Model):
    score = models.IntegerField()
    user = models.ForeignKey(User, related_name='bet_scores')
    bet = models.ForeignKey(Bet, related_name='bet_scores')

    def __unicode__(self):
        return unicode(self.score)
