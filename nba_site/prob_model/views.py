from django.shortcuts import render
from .pull_data import *
from .models import Team, Game, Schedule

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    update_day()
    return render(request, 'index.html', { 'all_teams': Team.objects.all()})

def teams(request):
    return render(request, 'teams.html',  {'teams': Team.objects.all()})

def games(request):
    return render(request, 'games.html',  {'games': Game.objects.all(), 'all_teams': Team.objects.all()})

def team_lookup(request):
    id = request.GET.get('id')
    team = Team.objects.get(team_id=id)
    schedule = Schedule.objects.get(team=team)
    games = schedule.games.all()  # Retrieve associated games
    return render(request, 'team_lookup.html', {'team': team, 'games': games, 'all_teams': Team.objects.all()})

def game_lookup(request):
    id = request.GET.get('id')
    game = Game.objects.get(game_id=id)
    return render(request, 'game_lookup.html', {'game': game, 'all_teams': Team.objects.all()})