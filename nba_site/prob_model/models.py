from django.db import models

class Team(models.Model):
    team_name = models.CharField(max_length=50)

class Game(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_games', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_games', on_delete=models.CASCADE)
    date = models.DateTimeField()
    location = models.CharField(max_length=100)




# Create your models here.
