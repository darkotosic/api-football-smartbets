# routers/today.py
from fastapi import APIRouter, HTTPException
from typing import List
import datetime

from smartbets_API.api_football import (
    get_fixtures,
    get_fixture_statistics,
    get_head_to_head,
    get_odds,
)
from models import (
    Fixture,
    FixtureStatistic,
    Head2HeadEntry,
    OddsResponse,
    TodayFixtureData,
)

router = APIRouter(prefix="/today", tags=["today"])

@router.get("/", response_model=List[TodayFixtureData])
async def read_today():
    today = datetime.date.today().isoformat()
    try:
        fx_payload = await get_fixtures(today)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    raw = fx_payload.get("response", [])
    fixtures = [Fixture.parse_obj(item) for item in raw]

    out: List[TodayFixtureData] = []
    for f in fixtures:
        fid = f.fixture.id

        stats_payload = await get_fixture_statistics(fid)
        stats = [FixtureStatistic.parse_obj(x) for x in stats_payload.get("response", [])]

        h2h_payload = await get_head_to_head(fid)
        h2h = [Head2HeadEntry.parse_obj(x) for x in h2h_payload.get("response", [])]

        odds_payload = await get_odds(fid)
        odds = [OddsResponse.parse_obj(x) for x in odds_payload.get("response", [])]

        out.append(TodayFixtureData(
            fixture=f,
            statistics=stats,
            h2h=h2h,
            odds=odds,
        ))

    return out
