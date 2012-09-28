# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from WettApp.bets.models import Bet, BetScore
from WettApp.bets.forms import NewBetForm
from django.contrib import messages


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
    try:
        bet_data = prepare_bet_data(request, bet_id)

        return render(request, 'bets/details.html', {'bet_data': bet_data})
    except:
        messages.error(request, 'You can not view Bets you are not involved in!')
        return HttpResponseRedirect('/bets/index')


@login_required
def new_bet(request):
    if request.method == 'POST':
        form = NewBetForm(request.POST, user=request.user)
        if form.is_valid():
            # we should take a look at this code looks ugly...
            form.save(request.user)
            messages.success(request, 'successfully added new bet')
            return HttpResponseRedirect('/bets/index')
    else:
        form = NewBetForm(user=request.user)
    return render(request, 'bets/new.html', {'form': form})


@login_required
def finish_bet(request, bet_id):
    try:
        bet_data = prepare_bet_data(request, bet_id)
        bet_data['yourself'][1].delete()
        bet_data['opponent'][1].delete()
        bet_data['bet'].delete()
        return render(request, 'bets/finish.html', {'bet_data': bet_data})
    except:
        messages.error(request, 'You can not end bets you are not involved in!')
        return HttpResponseRedirect('/bets/index')


def prepare_bet_data(request, bet_id):
    bet_data = {}
    current_bet = Bet.objects.get(id=bet_id)
    current_bet.participants.get(username=request.user.username)
    bet_data['bet'] = current_bet
    for participant in current_bet.participants.all():
        score = current_bet.participant_score(participant)
        if participant == request.user:
            bet_data['yourself'] = (participant, score)
        else:
            bet_data['opponent'] = (participant, score)
    return bet_data


def get_score_class(score_diff):
    if score_diff < 0:
        return "warning"
    elif score_diff > 0:
        return "good"
    else:
        return "undecided"
