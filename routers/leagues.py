# routers/leagues.py

from fastapi import APIRouter, HTTPException
from typing import List, Optional

from models import LeagueSeasonList
from smartbets_API.api_football import get_leagues, get_seasons

router = APIRouter(prefix="/leagues", tags=["leagues"])


@router.get("/", response_model=List[LeagueSeasonList])
async def read_leagues(
    country: Optional[str] = None
) -> List[LeagueSeasonList]:
    """
    Vraća listu liga.
    query params:
      - country: filter po ISO country code (npr. "England")
    """
    try:
        payload = await get_leagues(country)
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{league_id}/seasons", response_model=List[int])
async def read_seasons(
    league_id: int
) -> List[int]:
    """
    Vraća listu sezona za odabranu ligu.
    path params:
      - league_id: ID lige (npr. 39)
    """
    try:
        payload = await get_seasons(league_id)
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
