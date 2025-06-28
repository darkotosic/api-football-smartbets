from fastapi import APIRouter
from typing import List, Optional
from smartbets_API.api_football import (
    get_fixtures_rounds,
    get_fixtures,
    get_head2head,
    get_fixture_statistics,
    get_fixture_events,
)

router = APIRouter(prefix="/fixtures", tags=["fixtures-extra"])

@router.get("/rounds", response_model=List[dict])
async def read_rounds(league: int, season: int):
    data = await get_fixtures_rounds(league, season)
    return data.get("response", [])

@router.get("/", response_model=List[dict])
async def read_fixtures(
    date: Optional[str] = None,
    league: Optional[int] = None,
    season: Optional[int] = None,
    status: Optional[str] = None,
):
    data = await get_fixtures(date, league, season, status)
    return data.get("response", [])

@router.get("/head2head", response_model=List[dict])
async def read_h2h(team1: int, team2: int, season: Optional[int] = None):
    data = await get_head2head(team1, team2, season)
    return data.get("response", [])

@router.get("/{fixture_id}/statistics", response_model=List[dict])
async def read_fixture_stats(fixture_id: int, halftime: bool = False):
    data = await get_fixture_statistics(fixture_id, halftime)
    return data.get("response", [])

@router.get("/{fixture_id}/events", response_model=List[dict])
async def read_fixture_events(fixture_id: int):
    data = await get_fixture_events(fixture_id)
    return data.get("response", [])
