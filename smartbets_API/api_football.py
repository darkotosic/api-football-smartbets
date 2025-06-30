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

async def get_odds_by_fixture(
    fixture: int,
    bookmaker: Optional[int] = None
) -> Dict[str, Any]:
    params: Dict[str, Any] = {"fixture": fixture}
    if bookmaker is not None:
        params["bookmaker"] = bookmaker
    return await _get("/odds", params)

async def get_head2head(
    team1: int,
    team2: int,
    season: Optional[int] = None
) -> Dict[str, Any]:
    params: Dict[str, Any] = {"team1": team1, "team2": team2}
    if season is not None:
        params["season"] = season
    return await _get("/fixtures/headtohead", params)
