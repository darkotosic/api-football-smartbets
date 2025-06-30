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
async def get_today_data(
    league: Optional[int] = None,
    season: Optional[int] = None,
    bookmaker: Optional[int] = None,
):
    """Sve utakmice danas + kvote + H2H + vaša predikcija."""
    today_str = date.today().isoformat()

    try:
        # 1) Fixtures
        fx_payload = await get_fixtures_by_date(today_str, league, season)
        fixtures = fx_payload.get("response", [])

        # 2) Custom predictions za ceo dan
        predictor = Predictor(league=league, season=season, bookmaker=bookmaker)
        preds = await predictor.predict_by_date(today_str)
        pred_map = {p.fixture_id: p for p in preds}

        # 3) Sastavljamo result
        result: List[TodayFixtureData] = []
        for fx in fixtures:
            fid = fx["fixture"]["fixture_id"]

            # a) Odds
            odds_payload = await get_odds_by_fixture(fid, bookmaker)
            odds = odds_payload.get("response", [])

            # b) Head2Head
            home = fx["teams"]["home"]["id"]
            away = fx["teams"]["away"]["id"]
            h2h_payload = await get_head2head(home, away, season)
            h2h = h2h_payload.get("response", [])

            # c) Your prediction (may be None)
            pred = pred_map.get(fid)

            result.append(TodayFixtureData(
                fixture=fx,
                odds=odds,
                h2h=h2h,
                prediction=pred
            ))

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
