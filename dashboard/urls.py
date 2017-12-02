from django.conf.urls import url

from .views import (
    IndexView, TweetsView, AccountsView, HastagsView, musicfans,
    summary, accounts, hashtags, locations, quotes, polarities, tweets,
    LocationsView, QuotesView, PolaritiesView
)

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^summary/$', summary, name='summary'),
    url(r'^accounts/$', accounts, name='accounts'),
    url(r'^hashtags/$', hashtags, name='hashtags'),
    url(r'^locations/$', locations, name='locations'),
    url(r'^quotes/$', quotes, name='quotes'),
    url(r'^polarities/$', polarities, name='polarities'),
    url(r'^tweets/$', tweets, name='tweets'),
    url(r'^musicfans/$', musicfans, name='musicfans'),
    url(r'^ver-tweets/$', TweetsView.as_view(), name='tweets-view'),
    url(
        r'^ver-polaridades/$',
        PolaritiesView.as_view(),
        name='polarities-view'
    ),
    url(
        r'^ver-cuentas-involucradas/$',
        AccountsView.as_view(),
        name='accounts-view'
    ),
    url(
        r'^ver-hastags/$',
        HastagsView.as_view(),
        name='hashtags-view'
    ),
    url(
        r'^ver-ubicaciones/$',
        LocationsView.as_view(),
        name='locations-view'
    ),
    url(
        r'^ver-citas/$',
        QuotesView.as_view(),
        name='quotes-view'
    ),
]