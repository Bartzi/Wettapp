# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from WettApp.bets.forms import NewBetForm
from WettApp.bets.models import Bet, BetScore


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
    bet_data = prepare_bet_data(request, bet_id)
    return render(request, 'bets/details.html', {'bet_data': bet_data})


@login_required
def new_bet(request, opponent_id=None):
    if request.method == 'POST':
        form = NewBetForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'successfully added new bet')
            return redirect('index-bets')
    else:
        initial = {}
        if opponent_id:
            initial['opponent'] = User.objects.get(pk=opponent_id)
        form = NewBetForm(user=request.user, initial=initial)
    return render(request, 'bets/new.html', {'form': form})


@login_required
def finish_bet(request, bet_id):
    bet_data = prepare_bet_data(request, bet_id)
    bet_data['bet'].delete()
    return render(request, 'bets/finish.html', {'bet_data': bet_data})


@login_required
def increase_score(request):
    if request.is_ajax():
        your_score_id = request.POST["your_score_id"]
        opponent_score_id = request.POST["opponent_score_id"]
        opponent_bet_score = BetScore.objects.get(id=opponent_score_id)
        your_bet_score = BetScore.objects.get(id=your_score_id)
        if opponent_bet_score.bet != your_bet_score.bet:
            messages.error(request, 'hmm something went wrong!')
            return redirect('index-bets')
        if your_bet_score.user != request.user:
            return redirect('index-bets')
        opponent_bet_score.score += 1
        opponent_bet_score.save()
        return HttpResponse(opponent_bet_score.score)
    else:
        return redirect('index-bets')


def prepare_bet_data(request, bet_id):
    bet = get_object_or_404(Bet, id=bet_id, participants__pk=request.user.pk)
    bet_data = {'bet': bet}
    for participant in bet.participants.all():
        score = bet.participant_score(participant)
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
