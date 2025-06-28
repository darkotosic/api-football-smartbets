# api-football-smartbets/routers/predictions.py

from fastapi import APIRouter, HTTPException
from typing import List, Optional

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
    try:
        predictor = Predictor(league=league, season=season, bookmaker=bookmaker)
        return await predictor.predict_by_date(date)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
