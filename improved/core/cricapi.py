"""
RapidAPI - Cricbuzz Cricket API Helper
Smart caching included - 500 requests/month mein poora mahina chalega
"""
import requests
import time
from django.conf import settings

RAPIDAPI_HOST = "cricbuzz-cricket.p.rapidapi.com"
BASE_URL = f"https://{RAPIDAPI_HOST}"

_cache = {}
CACHE_LIVE    = 15    # 15 sec - match chal raha ho
CACHE_NO_LIVE = 900   # 15 min - koi match nahi
CACHE_SQUAD   = 300   # 5 min - squad info


def _headers():
    return {
        "x-rapidapi-key": settings.CRICAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }


def _get(endpoint, params=None, ttl=CACHE_LIVE):
    if params is None:
        params = {}

    cache_key = endpoint + str(sorted(params.items()))
    now = time.time()

    if cache_key in _cache:
        data, ts = _cache[cache_key]
        if now - ts < ttl:
            return data

    try:
        resp = requests.get(
            f"{BASE_URL}/{endpoint}",
            headers=_headers(),
            params=params,
            timeout=8
        )
        if resp.status_code == 200:
            data = resp.json()
            _cache[cache_key] = (data, now)
            return data
        return None
    except Exception:
        return None


def get_live_matches():
    """Saare live matches."""
    data = _get("matches/v1/live", ttl=CACHE_LIVE)
    if not data:
        return []
    return data.get('typeMatches', [])


def get_match_scorecard(match_id):
    """Live scorecard - batsman, bowler, runs, wickets sab."""
    data = _get(f"mcenter/v1/{match_id}/scard", ttl=CACHE_LIVE)
    if not data:
        return None
    return data


def get_match_info(match_id):
    """Match info - venue, teams, toss."""
    data = _get(f"mcenter/v1/{match_id}", ttl=CACHE_SQUAD)
    if not data:
        return None
    return data


def get_match_squad(match_id):
    """Playing XI / Squad."""
    data = _get(f"mcenter/v1/{match_id}/playing11", ttl=CACHE_SQUAD)
    if not data:
        return None
    return data


def get_upcoming_matches():
    """Upcoming matches."""
    data = _get("matches/v1/upcoming", ttl=CACHE_NO_LIVE)
    if not data:
        return []
    return data.get('typeMatches', [])
