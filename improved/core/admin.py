from django.contrib import admin
from .models import Team, Player, Match, News, PointsTable

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'country')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'role')
    list_filter = ('team', 'role')
    search_fields = ('name',)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('title', 'team1', 'team2', 'status', 'date')
    list_filter = ('status',)
    search_fields = ('title', 'venue')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(PointsTable)
class PointsTableAdmin(admin.ModelAdmin):
    list_display = ('team', 'matches', 'wins', 'losses', 'points', 'net_run_rate')
