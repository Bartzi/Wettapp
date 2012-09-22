from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

urlpatterns = patterns('WettApp.bets.views',
    url(ur'^$', RedirectView.as_view(url=u'index/'), name='root-bets'),
    url(ur'^index/$', 'index', name='index-bets'),
)