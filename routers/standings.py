# api-football-smartbets/routers/standings.py

from fastapi import APIRouter, HTTPException
from typing import List

from models import StandingEntry
from smartbets_API.api_football import get_standings

router = APIRouter(prefix="/standings", tags=["standings"])

@router.get("/", response_model=List[StandingEntry])
async def read_standings(league: int, season: int) -> List[StandingEntry]:
    try:
        payload = await get_standings(league, season)
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
