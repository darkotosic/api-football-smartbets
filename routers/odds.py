from fastapi import APIRouter
from typing import List
from smartbets_API.api_football import get_odds_by_fixture, get_odds_mapping, get_bookmakers

router = APIRouter(prefix="/odds", tags=["odds"])

@router.get("/", response_model=List[dict])
async def read_odds(fixture: int, bookmaker: int):
    data = await get_odds_by_fixture(fixture, bookmaker)
    return data.get("response", [])

@router.get("/mapping", response_model=List[dict])
async def read_mapping():
    data = await get_odds_mapping()
    return data.get("response", [])

@router.get("/bookmakers", response_model=List[dict])
async def read_bookmakers():
    data = await get_bookmakers()
    return data.get("response", [])
