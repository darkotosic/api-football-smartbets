# routers/odds.py

from fastapi import APIRouter, HTTPException
from typing import List

from models import OddsResponse, OddsMappingEntry, BookmakerInfo
from smartbets_API.api_football import (
    get_odds_by_fixture,
    get_odds_mapping,
    get_bookmakers
)

router = APIRouter(prefix="/odds", tags=["odds"])


@router.get("/", response_model=List[OddsResponse])
async def read_odds(fixture: int, bookmaker: int):
    """
    Враћа листу опција (bets) и шансе за дати fixture_id + bookmaker_id.
    query params:
      - fixture: ID утакмице
      - bookmaker: ID књадионице
    """
    try:
        payload = await get_odds_by_fixture(fixture, bookmaker)
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mapping", response_model=List[OddsMappingEntry])
async def read_mapping():
    """
    Враћа преслик (mapping) ставки (npr. '1', 'X', '2') у људски читљив облик.
    """
    try:
        payload = await get_odds_mapping()
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bookmakers", response_model=List[BookmakerInfo])
async def read_bookmakers():
    """
    Враћа листу књадионица које API-Football подржава.
    """
    try:
        payload = await get_bookmakers()
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
