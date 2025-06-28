# api-football-smartbets/routers/countries.py

from fastapi import APIRouter, HTTPException
from typing import List

from models import Country
from smartbets_API.api_football import get_countries

router = APIRouter(prefix="/countries", tags=["countries"])

@router.get("/", response_model=List[Country])
async def read_countries() -> List[Country]:
    try:
        payload = await get_countries()
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
