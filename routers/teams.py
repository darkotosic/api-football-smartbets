# api-football-smartbets/routers/teams.py

from fastapi import APIRouter, HTTPException
from typing import List

from models import Team, TeamStatistics
from smartbets_API.api_football import get_teams, get_team_statistics

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/", response_model=List[Team])
async def read_teams(league: int, season: int) -> List[Team]:
    try:
        payload = await get_teams(league, season)
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{team_id}/statistics", response_model=List[TeamStatistics])
async def read_team_stats(team_id: int, league: int, season: int) -> List[TeamStatistics]:
    try:
        payload = await get_team_statistics(team_id, league, season)
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
