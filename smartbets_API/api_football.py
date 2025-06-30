import os
from typing import Any, Dict, Optional
import httpx
from ._http import _get

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

# -- Countries ---------------------------------------------------------------
async def get_countries() -> Dict[str, Any]:
    """GET /countries"""
    return await _get("/countries")

# -- Leagues -----------------------------------------------------------------
async def get_leagues(country: Optional[str] = None) -> Dict[str, Any]:
    """GET /leagues?country=<country>"""
    params = {"country": country} if country else None
    return await _get("/leagues", params=params)

async def get_seasons(league: int) -> Dict[str, Any]:
    """GET /leagues/seasons?league=<league>"""
    return await _get("/leagues/seasons", params={"league": league})

# -- Teams -------------------------------------------------------------------
async def get_teams(league: int, season: int) -> Dict[str, Any]:
    """GET /teams?league=<league>&season=<season>"""
    return await _get("/teams", params={"league": league, "season": season})

async def get_team_statistics(team: int, league: int, season: int) -> Dict[str, Any]:
    """GET /teams/statistics?team=<team>&league=<league>&season=<season>"""
    return await _get("/teams/statistics", params={
        "team": team, "league": league, "season": season
    })

# -- Standings ---------------------------------------------------------------
async def get_standings(league: int, season: int) -> Dict[str, Any]:
    """GET /standings?league=<league>&season=<season>"""
    return await _get("/standings", params={"league": league, "season": season})

# -- Fixtures ----------------------------------------------------------------
async def get_fixtures_rounds(league: int, season: int) -> Dict[str, Any]:
    """GET /fixtures/rounds?league=<league>&season=<season>"""
    return await _get("/fixtures/rounds", params={"league": league, "season": season})

async def get_fixtures(
    date: Optional[str] = None,
    league: Optional[int] = None,
    season: Optional[int] = None,
    status: Optional[str] = None,
) -> Dict[str, Any]:
    """Opšti GET /fixtures sa parametrima date, league, season, status"""
    params = {}
    for k, v in (("date", date), ("league", league), ("season", season), ("status", status)):
        if v is not None:
            params[k] = v
    return await _get("/fixtures", params=params)

async def get_head2head(team1: int, team2: int, season: Optional[int] = None) -> Dict[str, Any]:
    """GET /fixtures/headtohead?team1=<>&team2=<>[&season=<>]"""
    params = {"team1": team1, "team2": team2}
    if season: params["season"] = season
    return await _get("/fixtures/headtohead", params=params)

async def get_fixture_statistics(fixture: int, halftime: bool = False) -> Dict[str, Any]:
    """GET /fixtures/statistics?fixture=<>&half=<0|1>"""
    return await _get("/fixtures/statistics", params={"fixture": fixture, "half": int(halftime)})

async def get_fixture_events(fixture: int) -> Dict[str, Any]:
    """GET /fixtures/events?fixture=<>"""
    return await _get("/fixtures/events", params={"fixture": fixture})

# -- Predictions (API-Football pre-match) -----------------------------------
async def get_api_predictions(
    fixture: int,
    bookmaker: Optional[int] = None
) -> Dict[str, Any]:
    """GET /predictions?fixture=<>&[bookmaker=<>]"""
    params = {"fixture": fixture}
    if bookmaker: params["bookmaker"] = bookmaker
    return await _get("/predictions", params=params)

# -- Odds (Pre-Match) --------------------------------------------------------
async def get_odds_by_fixture(
    fixture: int, bookmaker: Optional[int] = None
) -> Dict[str, Any]:
    """GET /odds?fixture=<>&[bookmaker=<>]"""
    params = {"fixture": fixture}
    if bookmaker: params["bookmaker"] = bookmaker
    return await _get("/odds", params=params)

async def get_odds_mapping() -> Dict[str, Any]:
    """GET /odds/mapping"""
    return await _get("/odds/mapping")

async def get_bookmakers() -> Dict[str, Any]:
    """GET /odds/bookmakers"""
    return await _get("/odds/bookmakers")

# NEW PART
async def get_fixtures_by_date(
    date: str,
    league: int | None = None,
    season: int | None = None,
) -> dict:
    params = {"date": date}
    if league is not None:
        params["league"] = league
    if season is not None:
        params["season"] = season
    return await _get("/fixtures", params)

async def get_odds_by_fixture(
    fixture: int,
    bookmaker: int | None = None,
) -> dict:
    params = {"fixture": fixture}
    if bookmaker is not None:
        params["bookmaker"] = bookmaker
    return await _get("/odds", params)

async def get_head2head(
    home: int,
    away: int,
    season: int | None = None,
) -> dict:
    params = {"h2h": f"{home}-{away}"}
    if season is not None:
        params["season"] = season
    return await _get("/fixtures/headtohead", params)
