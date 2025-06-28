from fastapi import APIRouter
from typing import List
from smartbets_API.api_football import get_countries

router = APIRouter(prefix="/countries", tags=["countries"])

@router.get("/", response_model=List[dict])
async def read_countries():
    data = await get_countries()
    return data.get("response", [])
