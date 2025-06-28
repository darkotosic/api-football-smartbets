from fastapi import APIRouter, HTTPException
from typing import Optional, List
from models import FixtureInfo
from smartbets_API.api_football import get_fixtures_by_date

router = APIRouter(prefix='/fixtures', tags=['fixtures'])

@router.get('/', response_model=List[FixtureInfo])
async def read_fixtures(
    date: str,
    league: Optional[int] = None,
    season: Optional[int] = None
):
    try:
        data = await get_fixtures_by_date(date, league, season)
        return data.get('response', [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- routers/predictions.py ---
from fastapi import APIRouter, HTTPException
from typing import Optional, List
from models import PredictionResponse
from smartbets_API.predictor import Predictor

router = APIRouter(prefix='/predictions', tags=['predictions'])

@router.get('/', response_model=List[PredictionResponse])
async def read_predictions(
    date: str,
    league: int,
    season: int,
    bookmaker: Optional[int] = None
):
    try:
        predictor = Predictor(league=league, season=season, bookmaker=bookmaker)
        return await predictor.predict_by_date(date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))