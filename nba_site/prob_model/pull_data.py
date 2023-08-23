import os
from datetime import datetime, timedelta
from prob_model.models import Team, Game, Schedule, Result, Sim, Prediction, GameSet, MostRecentDay
from django.db.models import Max
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
        game_obj = Game.objects.get(game_id=g['id'])
        game_obj.add_result(g)
        update_sim(game_obj)


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


def get_relevant_games():
    #return GameSet.objects.get(name='relevant').games.all()
    return Game.objects.all().filter(prediction__isnull=False)


# # #initial games loading
# # def get_games():
# #     response = api_get_games(season)
# #     response = response['response']
# #     for g in response:
# #         try:
# #             home_id = g['teams']['home']['id']
# #             away_id = g['teams']['visitors']['id']
# #             home_team = Team.objects.filter(team_id=home_id)[0]
# #             away_team = Team.objects.filter(team_id=away_id)[0]
#             #create new game
#             start = datetime.strptime(g['date']['start'], "%Y-%m-%dT%H:%M:%S.%fZ")
#             isPreSeason = (start < season_start)
#             print('start', start)
#             print('season_S', season_start)
#             if not isPreSeason:
#                 result = None
#                 # #add results if applicable

#                 new_game = Game(
#                     game_id = g['id'],
#                     home_team = home_team,
#                     away_team = away_team,
#                     date = g['date']['start'],
#                     location = g['arena']['name'],
#                     isCompleted = False,
#                     prediction = None,
#                     result = result
#                 )
#                 new_game.save()
#                 #add to both teams' schedule
#                 home_sched = Schedule.objects.filter(team=home_team)[0]
#                 away_sched = Schedule.objects.filter(team=away_team)[0]
#                 home_sched.games.add(new_game)
#                 away_sched.games.add(new_game)
#                 home_sched.save()
#                 away_sched.save()
#             else:
#                 print('preseason')
#         except:
#             print("Game Failed " + g['teams']['home']['name'] + " v " + g['teams']['visitors']['name'])

# #code to update the database daily with yesterdays results
# def update_day(today, tomorrow):
#     #try to make a gameset or load existing gameset
#     try:
#         print("trying to find relevant gameset")
#         gs = GameSet.objects.get(name='relevant')
#         gs.games.clear()
#     except:
#         print('making gameset')
#         gs = GameSet(
#             name='relevant'
#         )

#     response = api_get_games_on_date(today)
#     response = response['response']
#     for game in response:
#         try:
#             #find game in database
#             g = Game.objects.get(game_id=game['id'])
#             if game['scores']['visitors']['points'] > game['scores']['home']['points']:
#                 winner = g.away_team
#                 winner_score = game['scores']['visitors']['points']
#                 loser = g.home_team
#                 loser_score = game['scores']['home']['points']
#             else:
#                 winner = g.home_team
#                 winner_score = game['scores']['home']['points']
#                 loser = g.away_team
#                 loser_score = game['scores']['visitors']['points']
#             result = Result(
#                 winner = winner,
#                 loser = loser,
#                 winner_score = winner_score,
#                 loser_score = loser_score
#                 )
#             result.save()
#             g.isCompleted = True
#             g.result = result
#             g.save()
#             gs.games.add(g)
#             print('succesfully updated game id: ' + str(game['id']))
#             ##call update sim function here:
#             update_sim(g)
#             ##
#         except:
#             print("Game does not exist in system ")
#     print('...done')
#     #predictions for next day
#     # tomorrow = "2022-10-11"
#     print("making predictions for " + tomorrow + "...")
#     response = api_get_games_on_date(tomorrow)
#     response = response['response']
#     gamelist = []
#     for game in response:
#         try:
#             #find game in database
#             g = Game.objects.get(game_id=game['id'])
#             gamelist.append(g)
#             gs.games.add(g)
#         except:
#             print("Game does not exist in system... trying to add")
            # try:
            #     #try to create new game
            #     home_id = game['teams']['home']['id']
            #     away_id = game['teams']['visitors']['id']
            #     home = Team.objects.filter(team_id=home_id)[0]
            #     away = Team.objects.filter(team_id=away_id)[0]
            #     newgame = Game(
            #         game_id = game['id'],
            #         home_team = home,
            #         away_team = away,
            #         date = game['date']['start'],
            #         location = game['arena']['name'],
            #         isCompleted = False,
            #         prediction = None,
            #         result = None
            #     )
            #     newgame.save()
            #     gamelist.append(newgame)
            #     #add new game to schedules
            #     home_sched = Schedule.objects.filter(team=home)[0]
            #     away_sched = Schedule.objects.filter(team=home)[0]
            #     home_sched.games.add(newgame)
            #     away_sched.games.add(newgame)
            #     home_sched.save()
            #     away_sched.save()
            #     gs.games.add(newgame)
            # except:
            #     print('adding failed')
#     update_predictions(gamelist)
#     gs.save()
#     print("... done updating")


