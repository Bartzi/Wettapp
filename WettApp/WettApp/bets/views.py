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
        score_diff = 0
        for participant in bet.participants.all():
            score = bet.participant_score(participant)
            scores_list.append((participant, score))
            if participant == request.user:
                score_diff += score.score
            else:
                score_diff -= score.score
        bet_list.append((bet, scores_list, get_score_class(score_diff)))
    return render(request, 'bets/index.html', {'bet_list': bet_list})


@login_required
def details(request, bet_id):
    bet_data = {}
    current_bet = Bet.objects.get(id=bet_id)
    bet_data['bet'] = current_bet
    for participant in current_bet.participants.all():
        score = current_bet.participant_score(participant)
        if participant == request.user:
            bet_data['yourself'] = score
        else:
            bet_data['opponent'] = (participant, score)
    return render(request, 'bets/details.html', {'bet_data': bet_data})


def get_score_class(score_diff):
    if score_diff < 0:
        return "warning"
    else:
        return "good"
