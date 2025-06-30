# api-football-smartbets/smartbets_API/api_football.py

import os
import httpx
from typing import Any, Dict, Optional

# load key from env
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
if not API_FOOTBALL_KEY:
    raise RuntimeError("API_FOOTBALL_KEY environment variable is not set")

BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_FOOTBALL_KEY}

async def _get(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    url = f"{BASE_URL}{endpoint}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=HEADERS, params=params)
        resp.raise_for_status()
        return resp.json()

# ── 1. COUNTRIES ──────────────────────────────────────────────────────────────────
async def get_countries() -> Dict[str, Any]:
    return await _get("/countries")

# ── 2. LEAGUES ────────────────────────────────────────────────────────────────────
async def get_leagues(country: Optional[str] = None) -> Dict[str, Any]:
    params = {"country": country} if country else None
    return await _get("/leagues", params)

async def get_league_seasons(league_id: int) -> Dict[str, Any]:
    return await _get(f"/leagues/{league_id}/seasons")

# alias for your routers
get_seasons = get_league_seasons

# ── 3. TEAMS ──────────────────────────────────────────────────────────────────────
async def get_teams(league: int, season: int) -> Dict[str, Any]:
    return await _get("/teams", {"league": league, "season": season})

async def get_team_statistics(team: int, league: int, season: int) -> Dict[str, Any]:
    return await _get("/teams/statistics", {"team": team, "league": league, "season": season})

# ── 4. STANDINGS ─────────────────────────────────────────────────────────────────
async def get_standings(league: int, season: int) -> Dict[str, Any]:
    return await _get("/standings", {"league": league, "season": season})

# ── 5. FIXTURES ──────────────────────────────────────────────────────────────────
async def get_fixtures_by_date(
    date: str,
    league: Optional[int] = None,
    season: Optional[int] = None
) -> Dict[str, Any]:
    params: Dict[str, Any] = {"date": date}
    if league is not None:
        params["league"] = league
    if season is not None:
        params["season"] = season
    return await _get("/fixtures", params)

# ── 6. FIXTURE EXTRA ──────────────────────────────────────────────────────────────
async def get_fixture_statistics(fixture: int) -> Dict[str, Any]:
    return await _get(f"/fixtures/{fixture}/statistics")

async def get_head2head(
    team1: int,
    team2: int,
    season: Optional[int] = None
) -> Dict[str, Any]:
    params: Dict[str, Any] = {"team1": team1, "team2": team2}
    if season is not None:
        params["season"] = season
    return await _get("/fixtures/headtohead", params)

# ── 7. ODDS ────────────────────────────────────────────────────────────────────────
async def get_odds_by_fixture(
    fixture: int,
    bookmaker: Optional[int] = None
) -> Dict[str, Any]:
    params: Dict[str, Any] = {"fixture": fixture}
    if bookmaker is not None:
        params["bookmaker"] = bookmaker
    return await _get("/odds", params)

async def get_bookmakers() -> Dict[str, Any]:
    return await _get("/odds/bookmakers")

async def get_odds_mapping() -> Dict[str, Any]:
    return await _get("/odds/mapping")
