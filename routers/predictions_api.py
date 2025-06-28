# routers/predictions_api.py

from fastapi import APIRouter, HTTPException
from typing import List, Optional

from models import APIPrediction  # Pydantic model za API-Football 'Predictions'
from smartbets_API.api_football import get_api_predictions

router = APIRouter(prefix="/predictions-api", tags=["predictions-api"])


@router.get("/", response_model=List[APIPrediction])
async def read_api_predictions(
    fixture: int,
    bookmaker: Optional[int] = None
) -> List[APIPrediction]:
    """
    Vraća API-Football predikcije za zadati fixture.
    query params:
      - fixture: ID utakmice (obavezno)
      - bookmaker: ID kladionice (opciono)
    """
    try:
        payload = await get_api_predictions(fixture, bookmaker)
        return payload.get("response", [])
    except HTTPException:
        # Propagiramo specifične HTTP greške (400/404)
        raise
    except Exception as e:
        # Neočekivane greške tretiramo kao 500
        raise HTTPException(status_code=500, detail=str(e))
