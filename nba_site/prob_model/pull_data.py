import os
from datetime import datetime, timedelta
from prob_model.models import Team, Game, Schedule, Result, Sim, Prediction
from .stats import update_predictions, update_sim
from .apiget import api_get_standings, api_get_games, api_get_games_on_date
import time

testdate = "2022-09-15"
test_datetime = datetime.strptime(testdate, "%Y-%m-%d")
season = "2022"

#initial team and schedule loading
def get_teams():
    response = api_get_standings(season)
    print(response)
    res = response['response']
    
    for r in res:
        #add new team
        new_team = Team(
            team_name = r['team']['name'],
            team_id = r['team']['id'],
            team_logo = r['team']['logo']
            )
        print('here2')
        #add new schedule for team
        new_schedule = Schedule(
            team = new_team,
            name = r['team']['name'] + " Schedule"
        )
        #add new sim for team
        new_sim = Sim(
            team = new_team,
            rating = 1000,
            variance = 100
        )
        print('here1')
        #save
        new_team.save()
        new_schedule.save()
        new_sim.save()
        print('saved' + r['team']['name'])
    get_games()

#initial games loading
def get_games():
    response = api_get_games(season)
    response = response['response']
    for g in response:
        try:
            home_id = g['teams']['home']['id']
            away_id = g['teams']['visitors']['id']
            home_team = Team.objects.filter(team_id=home_id)[0]
            away_team = Team.objects.filter(team_id=away_id)[0]
            #create new game
            start = datetime.strptime(g['date']['start'], "%Y-%m-%dT%H:%M:%S.%fZ")
            isCompleted = (start < test_datetime)
            print(test_datetime, g['date']['start'])
            print(isCompleted)
            result = None
            # #add results if applicable
            if isCompleted:
                if g['scores']['visitors']['points'] > g['scores']['home']['points']:
                    winner = away_team
                    winner_score = g['scores']['visitors']['points']
                    loser = home_team
                    loser_score = g['scores']['home']['points']
                else:
                    winner = home_team
                    winner_score = g['scores']['home']['points']
                    loser = away_team
                    loser_score = g['scores']['visitors']['points']
                result = Result(
                    winner = winner,
                    loser = loser,
                    winner_score = winner_score,
                    loser_score = loser_score
                )
                result.save()
            new_game = Game(
                game_id = g['id'],
                home_team = home_team,
                away_team = away_team,
                date = g['date']['start'],
                location = g['arena']['name'],
                isCompleted = isCompleted,
                prediction = None,
                result = result
            )
            new_game.save()
            #add to both teams' schedule
            home_sched = Schedule.objects.filter(team=home_team)[0]
            away_sched = Schedule.objects.filter(team=away_team)[0]
            home_sched.games.add(new_game)
            away_sched.games.add(new_game)
            home_sched.save()
            away_sched.save()
        except:
            print("Game Failed " + g['teams']['home']['name'] + " v " + g['teams']['visitors']['name'])

#code to update the database daily with yesterdays results
def update_day(today, tomorrow):
    # current_date = "2022-10-10"
    response = api_get_games_on_date(today)
    response = response['response']
    for game in response:
        try:
            #find game in database
            g = Game.objects.get(game_id=game['id'])
            if game['scores']['visitors']['points'] > game['scores']['home']['points']:
                winner = g.away_team
                winner_score = game['scores']['visitors']['points']
                loser = g.home_team
                loser_score = game['scores']['home']['points']
            else:
                winner = g.home_team
                winner_score = game['scores']['home']['points']
                loser = g.away_team
                loser_score = game['scores']['visitors']['points']
            result = Result(
                winner = winner,
                loser = loser,
                winner_score = winner_score,
                loser_score = loser_score
                )
            result.save()
            g.isCompleted = True
            g.result = result
            g.save()
            print('succesfully updated game id: ' + str(game['id']))
            ##call update sim function here:
            update_sim(g)
            ##
        except:
            print("Game does not exist in system ")
    print('...done')
    #predictions for next day
    # tomorrow = "2022-10-11"
    print("making predictions for " + tomorrow + "...")
    response = api_get_games_on_date(tomorrow)
    response = response['response']
    gamelist = []
    for game in response:
        try:
            #find game in database
            g = Game.objects.get(game_id=game['id'])
            gamelist.append(g)
        except:
            print("Game does not exist in system... trying to add")
            try:
                #try to create new game
                home_id = game['teams']['home']['id']
                away_id = game['teams']['visitors']['id']
                home = Team.objects.filter(team_id=home_id)[0]
                away = Team.objects.filter(team_id=away_id)[0]
                newgame = Game(
                    game_id = game['id'],
                    home_team = home,
                    away_team = away,
                    date = game['date']['start'],
                    location = game['arena']['name'],
                    isCompleted = False,
                    prediction = None,
                    result = None
                )
                newgame.save()
                gamelist.append(newgame)
                #add new game to schedules
                home_sched = Schedule.objects.filter(team=home)[0]
                away_sched = Schedule.objects.filter(team=home)[0]
                home_sched.games.add(newgame)
                away_sched.games.add(newgame)
                home_sched.save()
                away_sched.save()
            except:
                print('adding failed')
    update_predictions(gamelist)
    print("... done updating")

def clean_db():
    Game.objects.all().delete()
    Schedule.objects.all().delete()
    Team.objects.all().delete()
    Prediction.objects.all().delete()
    Result.objects.all().delete()
    Sim.objects.all().delete()


def test_2022():
    clean_db()

    start_date = datetime(2022, 9, 29)
    end_date = datetime(2023, 6, 13)
    day_increment = timedelta(days=1)

    current_date = start_date
    date_list = []

    while current_date <= end_date:
        date_list.append(str(current_date.strftime('%Y-%m-%d')))
        current_date += day_increment

    get_teams()
    
    for i in range(len(date_list)):
        time.sleep(250)
        try:
            update_day(date_list[i], date_list[i+1])
        except:
            print("last day")






    
        
