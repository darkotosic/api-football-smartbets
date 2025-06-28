from fastapi import APIRouter
from typing import List
from smartbets_API.api_football import get_standings

router = APIRouter(prefix="/standings", tags=["standings"])

@router.get("/", response_model=List[dict])
async def read_standings(league: int, season: int):
    data = await get_standings(league, season)
    return data.get("response", [])
