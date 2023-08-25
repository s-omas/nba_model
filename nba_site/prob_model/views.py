from django.shortcuts import render
from .pull_data import *
from .models import Team, Game, Schedule
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import time

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render, redirect


def index(request):
    # call update function for testing
    #update_day("2022-11-17","2022-11-18")
    # #
    return redirect("/games")

def teams(request):
    return render(request, 'teams.html',  {'teams': Team.objects.all()})

def games(request):
    return render(request, 'games.html',  {'games': get_relevant_games(), 'all_teams': Team.objects.all()})

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
    for i in range(20):
        time.sleep(2.5)
        pull()
        predict()
        save_relevant_games()
        collect_model_info()
    return HttpResponse("100 day test completed.")

def model_info(request):
    info = ModelInfo.objects.get(name='5')
    rating_dict = info.rating_hist
    sims_dict = info.sim_info
    return render(request, 'model_info.html', {'rating_dict': rating_dict, 'sims_dict': sims_dict, 'all_teams': Team.objects.all()})

def user_is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(user_is_admin)
def admin_setup(request):
    initial_setup()
    predict()
    save_relevant_games()
    collect_model_info()
    return HttpResponse("Initial seaason setup completed.")


@login_required
@user_passes_test(user_is_admin)
def admin_pull(request):
    pull()
    predict()
    save_relevant_games()
    collect_model_info()
    return HttpResponse("Day update completed.")


@login_required
@user_passes_test(user_is_admin)
def admin_predict(request):
    predict()
    return HttpResponse("Day update completed.")