# routers/predictions.py

from fastapi import APIRouter, HTTPException
from typing import Optional, List

from models import PredictionResponse
from smartbets_API.predictor import Predictor

router = APIRouter(prefix="/predictions", tags=["predictions"])

@router.get("/", response_model=List[PredictionResponse])
async def read_predictions(
    date: str,
    league: int,
    season: int,
    bookmaker: Optional[int] = None
) -> List[PredictionResponse]:
    """
    Vraća predikcije za sve utakmice tog datuma.
    query params:
      - date: YYYY-MM-DD (obavezno)
      - league: ID lige (obavezno)
      - season: godina sezone (obavezno)
      - bookmaker: ID kladionice (opciono)
    """
    try:
        predictor = Predictor(league=league, season=season, bookmaker=bookmaker)
        predictions = await predictor.predict_by_date(date)
        return predictions
    except HTTPException:
        # Propagiramo specifične HTTP greške
        raise
    except Exception as e:
        # Ostalo tretiramo kao 500
        raise HTTPException(status_code=500, detail=str(e))
