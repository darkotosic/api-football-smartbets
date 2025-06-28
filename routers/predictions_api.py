# api-football-smartbets/routers/predictions_api.py

from fastapi import APIRouter, HTTPException
from typing import List, Optional

from models import APIPrediction
from smartbets_API.api_football import get_api_predictions

router = APIRouter(prefix="/predictions-api", tags=["predictions-api"])

@router.get("/", response_model=List[APIPrediction])
async def read_api_predictions(
    fixture: int,
    bookmaker: Optional[int] = None
) -> List[APIPrediction]:
    try:
        payload = await get_api_predictions(fixture, bookmaker)
        return payload.get("response", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
