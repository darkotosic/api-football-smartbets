import os
import httpx
from typing import Any, Dict, Optional

API_KEY = os.getenv("API_FOOTBALL_KEY")
if not API_KEY:
    raise RuntimeError("API_FOOTBALL_KEY not set")

BASE    = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}


async def _get(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    url = f"{BASE}{path}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=HEADERS, params=params, timeout=15.0)
        resp.raise_for_status()
        return resp.json()


# ─────────────────── COUNTRIES ───────────────────
async def get_countries():
    return await _get("/countries")


# ─────────────────── LEAGUES ─────────────────────
async def get_leagues(country: Optional[str] = None):
    return await _get("/leagues", {"country": country} if country else None)

async def get_league_seasons(league: int):
    return await _get(f"/leagues/{league}/seasons")

get_seasons = get_league_seasons            # alias


# ─────────────────── TEAMS ───────────────────────
async def get_teams(league: int, season: int):
    return await _get("/teams", {"league": league, "season": season})

async def get_team_statistics(team: int, league: int, season: int):
    return await _get("/teams/statistics",
                      {"team": team, "league": league, "season": season})


# ─────────────────── STANDINGS ───────────────────
async def get_standings(league: int, season: int):
    return await _get("/standings", {"league": league, "season": season})


# ─────────────────── FIXTURES ────────────────────
async def get_fixtures(date: str,
                       league: Optional[int] = None,
                       season: Optional[int] = None):
    params: Dict[str, Any] = {"date": date}
    if league is not None:  params["league"] = league
    if season is not None:  params["season"] = season
    return await _get("/fixtures", params)

get_fixtures_by_date = get_fixtures          # alias

async def get_fixtures_rounds(league: int, season: int):
    return await _get("/fixtures/rounds", {"league": league, "season": season})

async def get_fixture_statistics(fixture: int):
    return await _get("/fixtures/statistics", {"fixture": fixture})

async def get_fixture_events(fixture: int):
    return await _get("/fixtures/events", {"fixture": fixture})


# ─────────────────── HEAD-TO-HEAD ────────────────
async def get_head_to_head(fixture: int):
    return await _get("/fixtures/headtohead", {"fixture": fixture})

get_head2head = get_head_to_head             # alias


# ─────────────────── ODDS ────────────────────────
async def get_odds(fixture: int, bookmaker: Optional[int] = None):
    params = {"fixture": fixture}
    if bookmaker is not None:
        params["bookmaker"] = bookmaker
    return await _get("/odds", params)

get_odds_by_fixture = get_odds               # alias

async def get_odds_mapping():
    return await _get("/odds/mapping")

async def get_odds_bookmakers():
    return await _get("/odds/bookmakers")

# ——— алијас за routers/odds.py ———
get_bookmakers = get_odds_bookmakers

# ──────────────── API-FOOTBALL PREDICTIONS ───────
async def get_predictions_api(date: str, league: int, season: int):
    return await _get("/predictions",
                      {"date": date, "league": league, "season": season})

get_api_predictions = get_predictions_api    # alias за routers/predictions_api.py
