from django.contrib import admin
from prob_model.models import Team,Game,Schedule, Sim

class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'team_id')
    def load_teams(self, request, queryset):
        from .pull_data import get_teams  # Import your Python function
        get_teams()
        self.message_user(request, 'teams were added successfully.')
    load_teams.short_description = 'Load Teams'
    actions = [load_teams]

admin.site.register(Team, TeamAdmin)

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['name', 'games_count']
    def games_count(self, obj):
        return obj.games.count()
    games_count.short_description = 'Number of Games'
    actions=[]

admin.site.register(Schedule, ScheduleAdmin)

class GameAdmin(admin.ModelAdmin):
    actions=[]

admin.site.register(Game, GameAdmin)


class SimAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'variance']
    def name(self, obj):
        return obj.team.team_name
    actions=[]

admin.site.register(Sim, SimAdmin)
