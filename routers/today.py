# api-football-smartbets/routers/today.py

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import date

from models import TodayFixtureData
from smartbets_API.api_football import (
    get_fixtures_by_date,
    get_odds_by_fixture,
    get_head2head,
)
from smartbets_API.predictor import Predictor

router = APIRouter(prefix="/today", tags=["today"])

@router.get("/", response_model=List[TodayFixtureData])
async def read_today(
    league: Optional[int] = None,
    season: Optional[int] = None,
    bookmaker: Optional[int] = None,
):
    today_iso = date.today().isoformat()
    try:
        fx_payload = await get_fixtures_by_date(today_iso, league, season)
        fixtures = fx_payload.get("response", [])

        predictor = Predictor(league=league, season=season, bookmaker=bookmaker)
        preds = await predictor.predict_by_date(today_iso)
        pred_map = {p.fixture_id: p for p in preds}

        out: List[TodayFixtureData] = []
        for fx in fixtures:
            fid = fx["fixture"]["fixture_id"]
            odds = (await get_odds_by_fixture(fid, bookmaker)).get("response", [])
            h2h = (await get_head2head(
                fx["teams"]["home"]["id"],
                fx["teams"]["away"]["id"],
                season,
            )).get("response", [])
            pred = pred_map.get(fid)

            out.append(TodayFixtureData(
                fixture=fx,
                odds=odds,
                h2h=h2h,
                prediction=pred,
            ))
        return out

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
