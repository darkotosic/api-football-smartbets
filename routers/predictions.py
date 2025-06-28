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
):
    """
    Vraća predikcije za sve utakmice tog datuma.
    query params:
      - date: YYYY-MM-DD
      - league: ID lige (obavezno)
      - season: godina sezone (obavezno)
      - bookmaker: opcioni ID kladionice
    """
    try:
        predictor = Predictor(league=league, season=season, bookmaker=bookmaker)
        return await predictor.predict_by_date(date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
