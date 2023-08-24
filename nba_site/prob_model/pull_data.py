import os
from datetime import datetime, timedelta
from prob_model.models import Team, Game, Schedule, Result, Sim, Prediction, GameSet, MostRecentDay
from django.db.models import Max, F
from .apiget import api_get_standings, api_get_games, api_get_games_on_date
import time
from .helpers import *
from .stats import update_predictions, update_sim

def initial_setup():
    print("Starting inital setup: getting teams")
    #try:
    clean_db()
    response = api_get_standings(season_year)['response']
    for r in response:
        add_team(r)
    # try:
    print("Starting to add games into db")
    response = api_get_games(season_year)['response']
    for g in response:
        add_game(g)
    # except:
    #     print("Failed to load games into db")
    day = MostRecentDay(rd_id=0, day=0)
    day.save()


def pull():
    rd = MostRecentDay.objects.get(rd_id=0)
    n = rd.day
    day_str = generate_date_string(n)
    next_day_str = generate_date_string(n + 1)
    #get from api
    curr_res = api_get_games_on_date(day_str)['response']
    next_res = api_get_games_on_date(next_day_str)['response']
    #we only want games after 8am on curr, and before 8am on next (to account for time zone)
    day_games = [x for x in curr_res if not is_before_8am(x['date']['start'])]
    next_games = [x for x in next_res if is_before_8am(x['date']['start'])]
    games = day_games + next_games
    for g in games:
        try:
            game_obj = Game.objects.get(game_id=g['id'])
            game_obj.add_result(g)
            update_sim(game_obj)
        except:
            print('update failed')



def predict():
    rd = MostRecentDay.objects.get(rd_id=0)
    n = rd.day
    next_day_str = generate_date_string(n+1)
    second_day_str = generate_date_string(n+2)
    #get from api
    day1_games = api_get_games_on_date(next_day_str)['response']
    day2_games = api_get_games_on_date(second_day_str)['response']
    #we only want games after 8am on day1, before 8am on day2
    day1 = [x for x in day1_games if not is_before_8am(x['date']['start'])]
    day2 = [x for x in day2_games if is_before_8am(x['date']['start'])]
    all_games = day1 + day2
    update_predictions([Game.objects.get(game_id=x['id']) for x in all_games])
    rd.day = n+1
    rd.save()


def save_relevant_games():
    prediction_without_result = Game.objects.all().filter(prediction__isnull=False, result__isnull=True)
    games_with_results = Game.objects.filter(result__isnull=False).order_by('-game_id')[:10]
    try:
        gs = GameSet.objects.get(name='0')
        gs.games.clear()
    except:
        gs = GameSet(name='0')
    gs.save()
    for x in prediction_without_result:
        gs.games.add(x)
    for x in games_with_results:
        gs.games.add(x)
    gs.save()
    


def get_relevant_games():
    return GameSet.objects.get(name='0').games.all()
    #return Game.objects.all().filter(prediction__isnull=False)
