# routers/fixtures.py

from fastapi import APIRouter, HTTPException
from typing import Optional, List

from models import Fixture
from smartbets_API.api_football import get_fixtures_by_date

router = APIRouter(prefix="/fixtures", tags=["fixtures"])


@router.get("/", response_model=List[Fixture])
async def read_fixtures(
    date: str,
    league: Optional[int] = None,
    season: Optional[int] = None
) -> List[Fixture]:
    """
    Vraća listu utakmica (fixtures) za zadati datum.

    query params:
      - date: YYYY-MM-DD (obavezno)
      - league: opcioni ID lige
      - season: opcioni godina sezone (npr. 2025)
    """
    try:
        payload = await get_fixtures_by_date(date, league, season)
        return payload.get("response", [])
    except HTTPException:
        # Propagiramo HTTPException (npr. 404/422 iz sdk-a)
        raise
    except Exception as e:
        # Neočekivane greške pretvaramo u 500
        raise HTTPException(status_code=500, detail=str(e))
