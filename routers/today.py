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
    """
    Returns all fixtures for today + their odds + head2head + your prediction.
    """
    today_iso = date.today().isoformat()

    try:
        # 1) pull today's fixtures
        fx_payload = await get_fixtures_by_date(today_iso, league, season)
        fixtures = fx_payload.get("response", [])

        # 2) compute your predictions once
        predictor = Predictor(league=league, season=season, bookmaker=bookmaker)
        preds = await predictor.predict_by_date(today_iso)
        pred_map = {p.fixture_id: p for p in preds}

        # 3) build the list of TodayFixtureData
        out: List[TodayFixtureData] = []
        for fx in fixtures:
            fid = fx["fixture"]["fixture_id"]

            # odds
            odds_payload = await get_odds_by_fixture(fid, bookmaker)
            odds = odds_payload.get("response", [])

            # head2head
            h2h_payload = await get_head2head(
                fx["teams"]["home"]["id"],
                fx["teams"]["away"]["id"],
                season,
            )
            h2h = h2h_payload.get("response", [])

            # your pred if any
            pred = pred_map.get(fid)

            out.append(TodayFixtureData(
                fixture=fx,
                odds=odds,
                h2h=h2h,
                prediction=pred,
            ))

        return out

    except Exception as e:
        # catch-all
        raise HTTPException(status_code=500, detail=str(e))
