from fastapi import APIRouter
from typing import List, Optional
from smartbets_API.api_football import get_leagues, get_seasons

router = APIRouter(prefix="/leagues", tags=["leagues"])

@router.get("/", response_model=List[dict])
async def read_leagues(country: Optional[str] = None):
    data = await get_leagues(country)
    return data.get("response", [])

@router.get("/{league_id}/seasons", response_model=List[int])
async def read_seasons(league_id: int):
    data = await get_seasons(league_id)
    # response je lista sezona
    return data.get("response", [])
