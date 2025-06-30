# smartbets_API/api_football.py
import os
import httpx
from typing import Optional, Dict, Any

BASE = "https://api-football-smartbets.onrender.com"  # tvoj service root ako je reverse-proxy
API_FOOTBALL_URL = "https://v3.football.api-sports.io"  # original API-Football

API_KEY = os.getenv("API_FOOTBALL_KEY")  # Render env var

# interna funkcija za pozive
async def _get(path: str, params: Optional[Dict[str, Any]] = None):
    headers = {
        "x-apisports-key": API_KEY,
    }
    url = f"{API_FOOTBALL_URL}{path}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params, timeout=15.0)
        resp.raise_for_status()
        return resp.json()

# 1) COUNTRIES
async def get_countries():
    return await _get("/countries")

# 2) LEAGUES
async def get_leagues(country: Optional[str] = None):
    params = {"country": country} if country else None
    return await _get("/leagues", params)

async def get_league_seasons(league_id: int):
    return await _get("/leagues/seasons", {"league": league_id})

# 3) TEAMS
async def get_teams(league: int, season: int):
    return await _get("/teams", {"league": league, "season": season})

async def get_team_statistics(team: int, league: int, season: int):
    return await _get("/teams/statistics", {"team": team, "league": league, "season": season})

# 4) STANDINGS
async def get_standings(league: int, season: int):
    return await _get("/standings", {"league": league, "season": season})

# 5) FIXTURES
async def get_fixtures(date: str):
    return await _get("/fixtures", {"date": date})

async def get_fixtures_rounds(league: int, season: int):
    return await _get("/fixtures/rounds", {"league": league, "season": season})

async def get_fixture_statistics(fixture: int):
    return await _get("/fixtures/statistics", {"fixture": fixture})

async def get_fixture_events(fixture: int):
    return await _get("/fixtures/events", {"fixture": fixture})

async def get_head_to_head(fixture: int):
    return await _get("/fixtures/headtohead", {"fixture": fixture})

# 6) PREDICTIONS (custom)
# … ako koristiš interna predikcija, inače /predictions-api​
async def get_predictions_api(date: str, league: int, season: int):
    return await _get("/predictions-api", {"date": date, "league": league, "season": season})

# 7) ODDS
async def get_odds(fixture: int, bookmaker: Optional[int] = None):
    p = {"fixture": fixture}
    if bookmaker: p["bookmaker"] = bookmaker
    return await _get("/odds", p)

async def get_odds_mapping():
    return await _get("/odds/mapping")

async def get_odds_bookmakers():
    return await _get("/odds/bookmakers")
