from django.shortcuts import render
from .pull_data import *
from .models import Team, Game, Schedule

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # call update function for testing
    update_day("2022-10-17","2022-10-18")
    # ##
    return render(request, 'index.html', { 'all_teams': Team.objects.all()})

def teams(request):
    return render(request, 'teams.html',  {'teams': Team.objects.all()})

def games(request):
    return render(request, 'games.html',  {'games': Game.objects.filter(prediction__isnull=False), 'all_teams': Team.objects.all()})

def team_lookup(request):
    id = request.GET.get('id')
    team = Team.objects.get(team_id=id)
    schedule = Schedule.objects.get(team=team)

    games = schedule.games.filter(prediction__isnull=False)  # Retrieve associated games

    rating_hist = []
    for game in games:
        if team == game.home_team:
            rating_hist.append(game.prediction.home_team_rating)
        else:
            rating_hist.append(game.prediction.away_team_rating)


    return render(request, 'team_lookup.html', {'rating_history':rating_hist, 'team': team, 'games': games, 'all_teams': Team.objects.all()})

def game_lookup(request):
    id = request.GET.get('id')
    game = Game.objects.get(game_id=id)
    return render(request, 'game_lookup.html', {'game': game, 'all_teams': Team.objects.all()})

def test(request):
    test_2022()
    return render(request, 'teams.html',  {'teams': Team.objects.all()})

def model_info(request):
    rating_dict = {}
    all_teams = Team.objects.all()
    for team in all_teams:
        schedule = Schedule.objects.get(team=team)
        games = schedule.games.filter(prediction__isnull=False)  # Retrieve associated games

        rating_hist = []
        for game in games:
            if team == game.home_team:
                rating_hist.append(game.prediction.home_team_rating)
            else:
                rating_hist.append(game.prediction.away_team_rating)
        rating_dict.update({team.team_name: rating_hist})
    rating_dict = str(rating_dict)

    sims = Sim.objects.all()
    sims_dict = {}
    for s in sims:
        name = s.team.team_name
        rtg = s.rating
        var = s.variance
        sims_dict.update({name: {'variance': var, 'rating': rtg}})
    sims_dict = str(sims_dict)

    return render(request, 'model_info.html', {'rating_dict': rating_dict, 'sims_dict': sims_dict, 'all_teams': Team.objects.all()})