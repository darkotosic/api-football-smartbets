# api-football-smartbets/routers/fixtures_extra.py

from fastapi import APIRouter, HTTPException
from typing import List, Optional

from models import Round, Fixture, Head2HeadEntry, FixtureStatistic, FixtureEvent
from smartbets_API.api_football import (
    get_fixtures_rounds,
    get_fixtures,
    get_head2head,
    get_fixture_statistics,
    get_fixture_events,
)

router = APIRouter(prefix="/fixtures", tags=["fixtures-extra"])

@router.get("/rounds", response_model=List[Round])
async def read_rounds(league: int, season: int) -> List[Round]:
    try:
        payload = await get_fixtures_rounds(league, season)
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Fixture])
async def read_fixtures(
    date: Optional[str] = None,
    league: Optional[int] = None,
    season: Optional[int] = None,
    status: Optional[str] = None,
) -> List[Fixture]:
    try:
        payload = await get_fixtures(date, league, season, status)
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/head2head", response_model=List[Head2HeadEntry])
async def read_head2head(
    team1: int,
    team2: int,
    season: Optional[int] = None
) -> List[Head2HeadEntry]:
    try:
        payload = await get_head2head(team1, team2, season)
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{fixture_id}/statistics", response_model=List[FixtureStatistic])
async def read_fixture_statistics(
    fixture_id: int,
    halftime: bool = False
) -> List[FixtureStatistic]:
    try:
        payload = await get_fixture_statistics(fixture_id, halftime)
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{fixture_id}/events", response_model=List[FixtureEvent])
async def read_fixture_events(fixture_id: int) -> List[FixtureEvent]:
    try:
        payload = await get_fixture_events(fixture_id)
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
