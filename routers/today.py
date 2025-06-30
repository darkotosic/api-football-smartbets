from fastapi import APIRouter, HTTPException
from typing import List
from models import TodayFixture
from smartbets_API.api_football import get_fixtures_by_date, get_odds_by_fixture, get_fixture_statistics, get_head2head

router = APIRouter(prefix="/today", tags=["today"])

@router.get("/", response_model=List[TodayFixture])
async def read_today():
    import datetime
    today = datetime.date.today().isoformat()
    # 1) get all fixtures for today
    fx = await get_fixtures_by_date(today)
    fixtures = fx.get("response", [])

    results = []
    for f in fixtures:
        fid = f["fixture"]["fixture_id"]
        # 2) odds
        odds = (await get_odds_by_fixture(fid)).get("response", [])
        # 3) stats
        stats = (await get_fixture_statistics(fid)).get("response", [])
        # 4) h2h
        t1 = f["teams"]["home"]["id"]
        t2 = f["teams"]["away"]["id"]
        h2h = (await get_head2head(t1, t2)).get("response", [])
        results.append(TodayFixture(
            fixture=f,
            statistics=stats,
            head2head=h2h,
            odds=odds
        ))
    return results
