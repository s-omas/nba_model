import requests
import os
from prob_model.models import Team, Game, Schedule

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "key.txt")
with open(file_path, 'r') as file:
    k = file.read()

testdate = "2022-02-12"
season = "2022"


def get_teams():
    url = "https://api-nba-v1.p.rapidapi.com/standings"
    querystring = {"league":"standard","season":"2022"}
    headers = {
        "X-RapidAPI-Key": k,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    res = response.json()['response']
    
    for r in res:
        #add new team
        new_team = Team(
            team_name = r['team']['name'],
            team_id = r['team']['id'],
            team_logo = r['team']['logo']
            )
        #add new schedule for team
        new_schedule = Schedule(
            team = new_team,
            name = r['team']['name'] + " Schedule"
        )
        #save
        new_team.save()
        new_schedule.save()
        print('saved' + r['team']['name'])
    get_games()


def get_games():
    url = "https://api-nba-v1.p.rapidapi.com/games"
    querystring = {"season": season}
    headers = {
	    "X-RapidAPI-Key": k,
	    "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()['response']
    for g in response:
        try:
            home_id = g['teams']['home']['id']
            away_id = g['teams']['visitors']['id']
            home_team = Team.objects.filter(team_id=home_id)[0]
            away_team = Team.objects.filter(team_id=away_id)[0]
            #create new game
            new_game = Game(
                game_id = g['id'],
                home_team = home_team,
                away_team = away_team,
                date = g['date']['start'],
                location = g['arena']['name'],
                prediction = None,
                result = None
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
        
