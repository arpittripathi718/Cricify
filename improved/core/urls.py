from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('matches/', views.matches, name='matches'),
    path('matches/<int:pk>/', views.match_detail, name='match_detail'),
    path('news/', views.news, name='news'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('teams/', views.teams, name='teams'),
    path('teams/<int:pk>/', views.team_detail, name='team_detail'),
    path('players/', views.players, name='players'),
    path('players/<int:pk>/', views.player_detail, name='player_detail'),
    path('points-table/', views.points_table, name='points_table'),
    path('search/', views.search, name='search'),

    # Live Score Pages (CricAPI)
    path('live/', views.live_scores, name='live_scores'),
    path('live/<str:match_id>/', views.live_match_detail, name='live_match_detail'),

    # AJAX / JSON endpoints
    path('api/live-matches/', views.api_live_matches, name='api_live_matches'),
    path('api/live-score/<str:match_id>/', views.api_live_score, name='api_live_score'),
    path('api/points-table/', views.api_points_table, name='api_points_table'),
]
