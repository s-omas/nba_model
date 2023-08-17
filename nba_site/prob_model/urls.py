from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("teams", views.teams, name="teams"),
    path("games", views.games, name="games"),
    path('team_lookup/', views.team_lookup, name='team_lookup'),
]
