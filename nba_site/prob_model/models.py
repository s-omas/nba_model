from django.db import models

class Team(models.Model):
    team_name = models.CharField(max_length=50)
    team_id = models.IntegerField(default=99)
    team_logo = models.CharField(max_length=200)   


class Prediction(models.Model):
    expected_winner = models.ForeignKey(Team, related_name='prediction_expected_winner', on_delete=models.CASCADE)
    expected_loser = models.ForeignKey(Team, related_name='prediction_expected_loser', on_delete=models.CASCADE)
    winner_pct = models.FloatField()
    loser_pct = models.FloatField()
    home_team_rating = models.FloatField(default=1000)
    home_team_variance = models.FloatField(default=100)
    away_team_rating = models.FloatField(default=1000)
    away_team_variance = models.FloatField(default=100)

class Result(models.Model):
    winner = models.ForeignKey(Team, related_name='result_winner', on_delete=models.CASCADE)
    loser = models.ForeignKey(Team, related_name='result_loser', on_delete=models.CASCADE)
    winner_score = models.IntegerField()
    loser_score = models.IntegerField()

class Game(models.Model):
    game_id = models.IntegerField(default=0)
    home_team = models.ForeignKey(Team, related_name='home_games', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_games', on_delete=models.CASCADE)
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    isCompleted = models.BooleanField(default=False)
    isProcessed = models.BooleanField(default=False)
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE, null=True)
    result = models.ForeignKey(Result, on_delete=models.CASCADE, null=True)

    def add_result(self, response_dict):
        if response_dict['scores']['home']['points'] > response_dict['scores']['visitors']['points']:
            winner = self.home_team
            loser = self.away_team
        else:
            loser = self.home_team
            winner = self.away_team
        winscore = max(response_dict['scores']['home']['points'], response_dict['scores']['visitors']['points'])
        losscore = min(response_dict['scores']['home']['points'], response_dict['scores']['visitors']['points'])

        result = Result.objects.create(
            winner=winner, 
            loser=loser, 
            winner_score=winscore, 
            loser_score=losscore
        )
        self.result = result
        self.isCompleted = True
        self.save()


class Schedule(models.Model):
    name = models.CharField(max_length=50)
    team = models.ForeignKey(Team, related_name="team_schedule", on_delete=models.CASCADE)
    games = games = models.ManyToManyField(Game)

class Sim(models.Model):
    team = models.ForeignKey(Team, related_name="team_sim", on_delete=models.CASCADE)
    rating = models.FloatField(default=1000)
    variance = models.FloatField(default=100)

class GameSet(models.Model):
    name = models.CharField(max_length=20)
    games = models.ManyToManyField(Game)

    def rotate(self, new_game):
        # Add the new game to the set
        self.games.add(new_game)

        # Determine the game with the highest game_id and remove it
        game_to_remove = self.games.order_by('game_id').first()
        if game_to_remove:
            self.games.remove(game_to_remove)


class MostRecentDay(models.Model):
    rd_id = models.IntegerField(default=0)
    day = models.IntegerField()


class ModelInfo(models.Model):
    rating_hist = models.JSONField()
    sim_info = models.JSONField()
    name = models.CharField(max_length=2)
