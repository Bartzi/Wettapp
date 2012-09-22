from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from bets.models import Bet


@login_required
def index(request):
    user_bets = Bet.objects.filter(participants__contains=request.user)
    return render(request, 'bets/index.html', {'bets': user_bets})
