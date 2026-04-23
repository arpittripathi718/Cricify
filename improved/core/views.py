from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from .models import Match, News, Team, Player, PointsTable
from . import cricapi


def normalize_scorecard(raw_scorecard, info_data=None):
    if not raw_scorecard:
        return None

    innings_list = raw_scorecard.get("scorecard", [])
    if not innings_list:
        return None

    match_info = (info_data or {}).get("matchInfo", {}) if info_data else {}

    team1_name = (
        match_info.get("team1", {}).get("name")
        or (info_data or {}).get("team1", {}).get("teamName")
        or ""
    )
    team2_name = (
        match_info.get("team2", {}).get("name")
        or (info_data or {}).get("team2", {}).get("teamName")
        or ""
    )

    scorecard_list = []
    
    for inning in innings_list:
        batsman_list = []
        for bat in inning.get("batsman", []):
            batsman_list.append({
                "name": bat.get("name", ""),
                "runs": bat.get("runs", 0),
                "balls": bat.get("balls", 0),
                "fours": bat.get("fours", 0),
                "sixes": bat.get("sixes", 0),
                "strkrate": bat.get("strkrate", "0"),
                "outdec": bat.get("outdec", ""),
                "iscaptain": bat.get("iscaptain", False),
                "iskeeper": bat.get("iskeeper", False),
            })

        bowler_list = []
        for bowl in inning.get("bowler", []):
            bowler_list.append({
                "name": bowl.get("name", ""),
                "overs": bowl.get("overs", ""),
                "maidens": bowl.get("maidens", 0),
                "runs": bowl.get("runs", 0),
                "wickets": bowl.get("wickets", 0),
                "no_balls": 0,
                "wides": 0,
                "economy": bowl.get("economy", ""),
            })

        scorecard_list.append({
            "batteamname": inning.get("batteamname", ""),
            "score": inning.get("score", 0),
            "wickets": inning.get("wickets", 0),
            "overs": inning.get("overs", 0),
            "runrate": inning.get("runrate", 0),
            "isdeclared": inning.get("isdeclared", False),
            "batsman": batsman_list,
            "bowler": bowler_list,
            "extras": inning.get("extras", {}),
        })

    return {
        "matchHeader": {
            "team1": {"name": team1_name},
            "team2": {"name": team2_name},
            "seriesDesc": raw_scorecard.get("appindex", {}).get("seotitle", ""),
            "matchDescription": "",
            "status": raw_scorecard.get("status", ""),
        },
        "scorecard": scorecard_list
    }

def home(request):
    live_matches = Match.objects.filter(status='Live').order_by('-date')[:6]
    upcoming_matches = Match.objects.filter(status='Upcoming').order_by('date')[:6]
    latest_news = News.objects.order_by('-published_at')[:6]
    points = PointsTable.objects.select_related('team')[:10]
    context = {
        'live_matches': live_matches,
        'upcoming_matches': upcoming_matches,
        'latest_news': latest_news,
        'points': points,
    }
    return render(request, 'core/home.html', context)


def matches(request):
    all_matches = Match.objects.order_by('-date')
    return render(request, 'core/matches.html', {'matches': all_matches})


def match_detail(request, pk):
    match = get_object_or_404(Match, pk=pk)
    return render(request, 'core/match_detail.html', {'match': match})


def news(request):
    all_news = News.objects.order_by('-published_at')
    return render(request, 'core/news.html', {'news_list': all_news})


def news_detail(request, slug):
    article = get_object_or_404(News, slug=slug)
    recent_news = News.objects.exclude(slug=slug).order_by('-published_at')[:4]
    return render(request, 'core/news_detail.html', {'article': article, 'recent_news': recent_news})


def teams(request):
    all_teams = Team.objects.all()
    return render(request, 'core/teams.html', {'teams': all_teams})


def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    players = team.players.all()
    team1_matches = Match.objects.filter(team1=team).order_by('-date')[:5]
    team2_matches = Match.objects.filter(team2=team).order_by('-date')[:5]
    recent_matches = sorted(
        list(team1_matches) + list(team2_matches),
        key=lambda m: m.date, reverse=True
    )[:5]
    return render(request, 'core/team_detail.html', {
        'team': team,
        'players': players,
        'recent_matches': recent_matches,
    })


def players(request):
    all_players = Player.objects.select_related('team').all()
    teams = Team.objects.all()
    role_filter = request.GET.get('role', '')
    team_filter = request.GET.get('team', '')
    if role_filter:
        all_players = all_players.filter(role=role_filter)
    if team_filter:
        all_players = all_players.filter(team__id=team_filter)
    return render(request, 'core/players.html', {
        'players': all_players,
        'teams': teams,
        'role_filter': role_filter,
        'team_filter': team_filter,
    })


def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    teammates = Player.objects.filter(team=player.team).exclude(pk=pk)[:5]
    return render(request, 'core/player_detail.html', {
        'player': player,
        'teammates': teammates,
    })


def points_table(request):
    table = PointsTable.objects.select_related('team').all()
    return render(request, 'core/points_table.html', {'table': table})


def search(request):
    query = request.GET.get('q', '').strip()
    results = {'matches': [], 'news': [], 'teams': [], 'players': []}
    if query:
        results['matches'] = Match.objects.filter(
            Q(title__icontains=query) | Q(venue__icontains=query))[:5]
        results['news'] = News.objects.filter(
            Q(title__icontains=query) | Q(summary__icontains=query))[:5]
        results['teams'] = Team.objects.filter(
            Q(name__icontains=query) | Q(short_name__icontains=query))[:5]
        results['players'] = Player.objects.filter(
            Q(name__icontains=query)).select_related('team')[:5]
    return render(request, 'core/search.html', {'results': results, 'query': query})


# ===== LIVE SCORE VIEWS (RapidAPI Cricbuzz) =====

def live_scores(request):
    """Saare live matches dikhao."""
    type_matches = cricapi.get_live_matches()

    # typeMatches ke andar seriesMatches ke andar matches hote hain
    all_matches = []
    for tm in type_matches:
        for sm in tm.get('seriesMatches', []):
            series_wrapper = sm.get('seriesAdWrapper') or sm
            for m in series_wrapper.get('matches', []):
                match_info = m.get('matchInfo', {})
                match_score = m.get('matchScore', {})
                all_matches.append({
                    'id': match_info.get('matchId'),
                    'desc': match_info.get('matchDesc', ''),
                    'series': match_info.get('seriesName', ''),
                    'team1': match_info.get('team1', {}).get('teamName', ''),
                    'team2': match_info.get('team2', {}).get('teamName', ''),
                    'venue': match_info.get('venueInfo', {}).get('ground', ''),
                    'state': match_info.get('state', ''),
                    'status': match_info.get('status', ''),
                    'score': match_score,
                })

    return render(request, 'core/live_scores.html', {'matches': all_matches})


def live_match_detail(request, match_id):
    """Ek match ka poora scorecard + squad."""
    raw_scorecard = cricapi.get_match_scorecard(match_id)
    squad_data = cricapi.get_match_squad(match_id)
    info_data = cricapi.get_match_info(match_id)

    scorecard_data = normalize_scorecard(raw_scorecard, info_data)

    return render(request, 'core/live_match_detail.html', {
        'scorecard': scorecard_data,
        'squad': squad_data,
        'info': info_data,
        'match_id': match_id,
    })

   


def api_live_score(request, match_id):
    """JSON endpoint — frontend har 2 min mein ye call karta hai."""
    raw_scorecard = cricapi.get_match_scorecard(match_id)
    info_data = cricapi.get_match_info(match_id)
    data = normalize_scorecard(raw_scorecard, info_data)

    if not data:
        return JsonResponse({'error': 'Score fetch failed'}, status=503)

    return JsonResponse(data, safe=False)


def api_live_matches(request):
    """JSON — saare live matches."""
    type_matches = cricapi.get_live_matches()
    return JsonResponse({'typeMatches': type_matches}, safe=False)


def api_points_table(request):
    """JSON — Points table live update."""
    table = PointsTable.objects.select_related('team').all().order_by('-points', '-net_run_rate')
    data = []
    for row in table:
        data.append({
            'team_name': row.team.name,
            'matches': row.matches,
            'wins': row.wins,
            'losses': row.losses,
            'points': row.points,
            'net_run_rate': row.net_run_rate,
        })
    return JsonResponse({'table': data}, safe=False)
