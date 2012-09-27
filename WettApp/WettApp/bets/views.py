# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from WettApp.bets.models import Bet, BetScore
from WettApp.bets.forms import NewBetForm
from WettApp.users.models import UserProfile
from django.contrib import messages
import datetime


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
    user_found = False
    for participant in current_bet.participants.all():
        score = current_bet.participant_score(participant)
        if participant.user == request.user:
            bet_data['yourself'] = score
            user_found = True
        else:
            bet_data['opponent'] = (participant, score)
    if not user_found:
        messages.error(request, 'Do not try to view content that does not belong to you!')
        return HttpResponseRedirect('/bets/index')
    return render(request, 'bets/details.html', {'bet_data': bet_data})


@login_required
def new_bet(request):
    if request.method == 'POST':
        cancel = request.POST.get('cancel', None)
        if cancel:
            return HttpResponseRedirect('bets/index.html')
        form = NewBetForm(request.POST, user=request.user)
        if form.is_valid():
            # we should take a look at this code looks ugly...
            new_bet = Bet()
            new_bet.title = form.cleaned_data['title']
            new_bet.start_date = datetime.datetime.now()
            new_bet.description = form.cleaned_data['description']
            new_bet.save()
            new_bet.participants.add(request.user, form.cleaned_data['opponent'])
            new_bet.save()
            bet_score = BetScore()
            bet_score.score = 0
            bet_score.user = request.user
            bet_score.bet = new_bet
            bet_score.save()
            bet_score = BetScore()
            bet_score.score = 0
            bet_score.user = form.cleaned_data['opponent']
            bet_score.bet = new_bet
            bet_score.save()
            messages.success(request, 'successfully added new bet')
            return HttpResponseRedirect('/bets/index')
    else:
        form = NewBetForm(user=request.user)
    return render(request, 'bets/new.html', {'form': form})


def get_score_class(score_diff):
    if score_diff < 0:
        return "warning"
    elif score_diff > 0:
        return "good"
    else:
        return "undecided"
