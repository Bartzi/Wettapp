from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Bet(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    startDate = models.DateTimeField('start Date')
    participants = models.ManyToManyField(User)


class BetScore(models.Model):
    score = models.IntegerField()
    user = models.ForeignKey(User)
    bet = models.ForeignKey(Bet)
