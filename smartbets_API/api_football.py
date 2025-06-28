import os
from typing import Any, Dict, Optional
import httpx

# Učitaj ključ iz okružnja
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
if not API_FOOTBALL_KEY:
    raise RuntimeError("API_FOOTBALL_KEY environment variable is not set")

# Osnovni URL za API-FOOTBALL v3
BASE_URL = "https://v3.football.api-sports.io"

# Zaglavlja koja se prosleđuju svakoj API-pozivu
HEADERS = {
    "x-apisports-key": API_FOOTBALL_KEY
}

async def _get(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Interna helper funkcija za GET pozive prema API-FOOTBALL.
    endpoint: putanja iza BASE_URL, npr. '/fixtures'
    params: query parametri
    """
    url = f"{BASE_URL}{endpoint}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()

async def get_fixtures_by_date(
    date: str,
    league: Optional[int] = None,
    season: Optional[int] = None
) -> Dict[str, Any]:
    """
    Vraća listu utakmica za dati datum.
    date: YYYY-MM-DD
    league: opciono ID lige
    season: opciono godina sezone
    """
    params: Dict[str, Any] = {"date": date}
    if league:
        params["league"] = league
    if season:
        params["season"] = season
    return await _get("/fixtures", params)

async def get_odds_by_fixture(
    fixture_id: int,
    bookmaker: Optional[int] = None
) -> Dict[str, Any]:
    """
    Vraća listu kvota za zadatu utakmicu.
    fixture_id: ID utakmice
    bookmaker: opciono ID kladionice (npr. 1=Bet365)
    """
    params: Dict[str, Any] = {"fixture": fixture_id}
    if bookmaker:
        params["bookmaker"] = bookmaker
    return await _get("/odds", params)

async def get_team_statistics(
    team_id: int,
    league: int,
    season: int
) -> Dict[str, Any]:
    """
    Vraća statistike tima u okviru odabrane lige i sezone.
    team_id: ID tima
    league: ID lige
    season: godina sezone
    """
    params = {"team": team_id, "league": league, "season": season}
    return await _get("/teams/statistics", params)

async def get_standings(
    league: int,
    season: int,
    timezone: Optional[str] = None
) -> Dict[str, Any]:
    """
    Vraća tabelu (standings) za zadatu ligu i sezonu.
    league: ID lige
    season: godina sezone
    timezone: opciono, za lokalizaciju vremena
    """
    params = {"league": league, "season": season}
    if timezone:
        params["timezone"] = timezone
    return await _get("/standings", params)

async def get_head_to_head(
    team: int,
    opponent: int
) -> Dict[str, Any]:
    """
    Vraća istoriju meč-eva između dva tima.
    team: ID prvog tima
    opponent: ID protivnika
    """
    params = {"team": team, "opponent": opponent}
    return await _get("/fixtures/headtohead", params)
