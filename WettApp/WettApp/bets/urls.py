# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.views.generic import RedirectView

urlpatterns = patterns('WettApp.bets.views',
    url(ur'^$', RedirectView.as_view(url=u'index/'), name='root-bets'),
    url(ur'^index/$', 'index', name='index-bets'),
    url(ur'^details/(?P<bet_id>\d+)/$', 'details', name='bet-details'),
    url(ur'^new/$', 'new_bet', name='new-bet'),
    url(ur'^new/(?P<opponent_id>\d+)/$', 'new_bet', name='new-bet'),
    url(ur'^finish/(?P<bet_id>\d+)/$', 'finish_bet', name='finish-bet'),
    url(ur'increase/$', 'increase_score'),
)
