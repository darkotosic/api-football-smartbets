# api-football-smartbets/routers/leagues.py

from fastapi import APIRouter, HTTPException
from typing import List, Optional

from models import League, LeagueSeasonList
from smartbets_API.api_football import get_leagues, get_league_seasons

router = APIRouter(prefix="/leagues", tags=["leagues"])

@router.get("/", response_model=List[League])
async def read_leagues(country: Optional[str] = None) -> List[League]:
    try:
        payload = await get_leagues(country)
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{league_id}/seasons", response_model=LeagueSeasonList)
async def read_league_seasons(league_id: int) -> LeagueSeasonList:
    try:
        payload = await get_league_seasons(league_id)
        resp = payload.get("response", [])
        if not resp:
            raise HTTPException(status_code=404, detail="League not found")
        league_info = resp[0].get("league", {})
        seasons = [s.get("season") for s in resp]
        return LeagueSeasonList(
            league=League.parse_obj(league_info),
            seasons=seasons
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
