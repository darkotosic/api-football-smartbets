# routers/countries.py

from fastapi import APIRouter
from typing import List
from models import Country
from smartbets_API.api_football import get_countries

router = APIRouter(prefix="/countries", tags=["countries"])

@router.get("/", response_model=List[Country])
async def read_countries():
    payload = await get_countries()
    return payload.get("response", [])
