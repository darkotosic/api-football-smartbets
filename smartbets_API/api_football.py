# smartbets_API/api_football.py
import os
import httpx
from typing import Any, Dict, Optional

API_KEY = os.getenv("API_FOOTBALL_KEY")
if not API_KEY:
    raise RuntimeError("API_FOOTBALL_KEY not set")

BASE = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}


async def _get(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    url = f"{BASE}{path}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=HEADERS, params=params)
        resp.raise_for_status()
        return resp.json()


# 1. COUNTRIES
async def get_countries() -> Dict[str, Any]:
    return await _get("/countries")


# 2. LEAGUES
async def get_leagues(country: Optional[str] = None) -> Dict[str, Any]:
    params = {"country": country} if country else None
    return await _get("/leagues", params)

async def get_league_seasons(league: int) -> Dict[str, Any]:
    return await _get(f"/leagues/{league}/seasons")

# alias for routers/leagues
get_seasons = get_league_seasons


# 3. TEAMS
async def get_teams(league: int, season: int) -> Dict[str, Any]:
    return await _get("/teams", {"league": league, "season": season})

async def get_team_statistics(team: int, league: int, season: int) -> Dict[str, Any]:
    return await _get("/teams/statistics", {"team": team, "league": league, "season": season})


# 4. STANDINGS
async def get_standings(league: int, season: int) -> Dict[str, Any]:
    return await _get("/standings", {"league": league, "season": season})


# 5. FIXTURES
async def get_fixtures(date: str) -> Dict[str, Any]:
    return await _get("/fixtures", {"date": date})

# alias for predictor.py import
get_fixtures_by_date = get_fixtures

async def get_fixtures_rounds(league: int, season: int) -> Dict[str, Any]:
    return await _get("/fixtures/rounds", {"league": league, "season": season})

async def get_fixture_statistics(fixture: int) -> Dict[str, Any]:
    return await _get("/fixtures/statistics", {"fixture": fixture})

async def get_fixture_events(fixture: int) -> Dict[str, Any]:
    return await _get("/fixtures/events", {"fixture": fixture})

async def get_head_to_head(fixture: int) -> Dict[str, Any]:
    return await _get("/fixtures/headtohead", {"fixture": fixture})


# 6. PREDICTIONS-API (if used)
async def get_predictions_api(date: str, league: int, season: int) -> Dict[str, Any]:
    return await _get("/predictions", {"date": date, "league": league, "season": season})


# 7. ODDS
async def get_odds(fixture: int, bookmaker: Optional[int] = None) -> Dict[str, Any]:
    params = {"fixture": fixture}
    if bookmaker is not None:
        params["bookmaker"] = bookmaker
    return await _get("/odds", params)

# alias for routers that import get_odds_by_fixture
get_odds_by_fixture = get_odds

async def get_odds_mapping() -> Dict[str, Any]:
    return await _get("/odds/mapping")

async def get_odds_bookmakers() -> Dict[str, Any]:
    return await _get("/odds/bookmakers")
