import pytz
from dateutil import parser
from prob_model.models import Team, Game, Schedule, Result, Sim, Prediction, GameSet, MostRecentDay, ModelInfo
from datetime import datetime, timedelta, time
from .stats import update_sim, make_prediction

season_year = "2022"
season_start_str = "2022-10-17"
season_end_str = "2023-06-15"
season_start = datetime.strptime(season_start_str, "%Y-%m-%d")
season_end = datetime.strptime(season_end_str, "%Y-%m-%d")


def convert_to_eastern_time(utc_time_str):
    # Parse the UTC time string
    utc_time = parser.isoparse(utc_time_str)

    # Define timezones for Eastern Time
    eastern_timezone = pytz.timezone('US/Eastern')

    # Convert UTC time to Eastern Time
    eastern_time = utc_time.astimezone(eastern_timezone)
    
    return eastern_time


def generate_date_string(days):
    try:
        new_date = season_start + timedelta(days=days)
        new_date_str = new_date.strftime("%Y-%m-%d")
        return new_date_str
    except ValueError:
        return "Invalid date format"
    

def is_datetime_in_past(dt):
    # # Get the current time in the Eastern Time zone
    # eastern_time = pytz.timezone('US/Eastern')
    # current_time = datetime.now(eastern_time)

    target_time = datetime(2022, 10, 18, 4, 0) # use this for testing - start at seasonstart

    # Set the timezone to Eastern Time (US/Eastern)
    eastern_time = pytz.timezone('US/Eastern')
    current_time = eastern_time.localize(target_time)
    
    return dt < current_time


def clean_db():
    Game.objects.all().delete()
    Schedule.objects.all().delete()
    Team.objects.all().delete()
    Prediction.objects.all().delete()
    Result.objects.all().delete()
    Sim.objects.all().delete()
    GameSet.objects.all().delete()
    MostRecentDay.objects.all().delete()
    ModelInfo.objects.all().delete()


#add team and associated items to db: Team, Sim, Schedule
def add_team(team_response):
    new_team = Team(
    team_name = team_response['team']['name'],
    team_id = team_response['team']['id'],
    team_logo = team_response['team']['logo']
    )
    #add new schedule for team
    new_schedule = Schedule(
        team = new_team,
        name = team_response['team']['name'] + " Schedule"
    )
    #add new sim for team
    new_sim = Sim(
        team = new_team,
        rating = 1000,
        variance = 500
    )
    new_team.save()
    new_schedule.save()
    new_sim.save()
    print("Saved team, schedule, sim for: " + new_team.team_name)


def add_game(game_res):
    print("trying to add new game")
    try:
        home_id = game_res['teams']['home']['id']
        away_id = game_res['teams']['visitors']['id']
        home_team = Team.objects.filter(team_id=home_id)[0]
        away_team = Team.objects.filter(team_id=away_id)[0]
        start = datetime.strptime(game_res['date']['start'], "%Y-%m-%dT%H:%M:%S.%fZ")
        isPreSeason = (start < season_start)
        print('start', start)
        print('season_S', season_start)
        if not isPreSeason:
            result = None
            # #add results if applicable

            new_game = Game(
                game_id = game_res['id'],
                home_team = home_team,
                away_team = away_team,
                date = game_res['date']['start'],
                location = game_res['arena']['name'],
                isCompleted = False,
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
        else:
            print("Is preseason game")
    except:
        print("game adding failed for game" + str(game_res['id']))


def day_game_update(game_res):
    id = game_res['id']
    try:

        print('looking for game: ' + str(id))
        game_record = Game.objects.get(game_id=id)
        gamestart = convert_to_eastern_time(game_res['date']['start'])
        #if game has happened
        if is_datetime_in_past(gamestart):
            # prev_completed = game_record.isCompleted
            # if not prev_completed:
            if game_res['scores']['visitors']['points'] > game_res['scores']['home']['points']:
                winner = game_record.away_team
                winner_score = game_res['scores']['visitors']['points']
                loser = game_record.home_team
                loser_score = game_res['scores']['home']['points']
            else:
                winner = game_record.home_team
                winner_score = game_res['scores']['home']['points']
                loser = game_record.away_team
                loser_score = game_res['scores']['visitors']['points']
            result = Result(
                winner = winner,
                loser = loser,
                winner_score = winner_score,
                loser_score = loser_score
                )
            result.save()
            game_record.isCompleted = True
            game_record.result = result
            game_record.save()
            update_sim(game_record)
            return game_record
        else:
            #game is in future
            if not game_record.prediction:
                new_pred = make_prediction(game_record)
                new_pred.save()
                game_record.prediction = new_pred
                game_record.save()

    except:
        print('not in database, trying to make game entry')
        try:
            #try to create new game
            home_id = game_res['teams']['home']['id']
            away_id = game_res['teams']['visitors']['id']
            home = Team.objects.filter(team_id=home_id)[0]
            away = Team.objects.filter(team_id=away_id)[0]
            game_record = Game(
                game_id = game_res['id'],
                home_team = home,
                away_team = away,
                date = game_res['date']['start'],
                location = game_res['arena']['name'],
                isCompleted = False,
                prediction = None,
                result = None
            )
            game_record.save()
            #add new game to schedules
            home_sched = Schedule.objects.filter(team=home)[0]
            away_sched = Schedule.objects.filter(team=home)[0]
            home_sched.games.add(game_record)
            away_sched.games.add(game_record)
            home_sched.save()
            away_sched.save()
            new_pred = make_prediction(game_record)
            new_pred.save()
            game_record.prediction = new_pred
            game_record.save()
        except:
            print('adding failed')
    game_record.save()
    return game_record


def is_before_8am(dt_str):
    dt = datetime.fromisoformat(dt_str[:-1])
    eight_am = time(8, 0, 0)
    return dt.time() < eight_am


def collect_model_info():
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
    sims = Sim.objects.all()
    sims_dict = {}
    for s in sims:
        name = s.team.team_name
        rtg = round(s.rating, 1)
        var = round(s.variance, 1)
        sims_dict.update({name: {'variance': var, 'rating': rtg}})

    ModelInfo.objects.all().delete()
    info = ModelInfo.objects.create(
        name='5',
        rating_hist = rating_dict,
        sim_info=sims_dict
    )
    info.save()
    


