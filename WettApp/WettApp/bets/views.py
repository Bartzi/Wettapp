# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from WettApp.bets.models import Bet


@login_required
def index(request):
    user_bets = Bet.objects.filter(participants__in=[request.user])
    bet_list = []
    for bet in user_bets:
        scores_list = []
        for participant in bet.participants.all():
            score = bet.participant_score(participant)
            scores_list.append((participant, score))
        bet_tuple = (bet, scores_list)
        bet_list.append(bet_tuple)

    return render(request, 'bets/index.html', {'bet_list': bet_list})
