from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("teams", views.teams, name="teams"),
    path("games", views.games, name="games"),
    path('team_lookup/', views.team_lookup, name='team_lookup'),
    path('game_lookup/', views.game_lookup, name='game_lookup'),
    path('test/', views.test, name='test'),
    path('model/', views.model_info, name='modelinfo'),
    path('admin-setup/', views.admin_setup, name='admin_setup'),
    path('admin-update/', views.admin_update, name='admin_update'),
]
