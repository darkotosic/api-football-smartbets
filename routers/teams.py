from fastapi import APIRouter
from typing import List, Optional
from smartbets_API.api_football import get_teams, get_team_statistics

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/", response_model=List[dict])
async def read_teams(league: int, season: int):
    data = await get_teams(league, season)
    return data.get("response", [])

@router.get("/{team_id}/statistics", response_model=List[dict])
async def read_team_stats(team_id: int, league: int, season: int):
    data = await get_team_statistics(team_id, league, season)
    return data.get("response", [])
