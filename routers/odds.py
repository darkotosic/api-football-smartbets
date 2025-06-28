# api-football-smartbets/routers/odds.py

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
async def read_odds(fixture: int, bookmaker: int) -> List[OddsResponse]:
    try:
        payload = await get_odds_by_fixture(fixture, bookmaker)
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mapping", response_model=List[OddsMappingEntry])
async def read_mapping() -> List[OddsMappingEntry]:
    try:
        payload = await get_odds_mapping()
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/bookmakers", response_model=List[BookmakerInfo])
async def read_bookmakers() -> List[BookmakerInfo]:
    try:
        payload = await get_bookmakers()
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
