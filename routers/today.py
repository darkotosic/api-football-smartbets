# routers/today.py
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import datetime

from smartbets_API.api_football import (
    get_fixtures,
    get_fixture_statistics,
    get_head_to_head,
    get_odds,
)

router = APIRouter(prefix="/today", tags=["today"])

@router.get("/", response_model=List[Dict[str, Any]])      # ⇦ vraćamo listu dict-ova
async def read_today():
    date_str = datetime.date.today().isoformat()
    try:
        fx_payload = await get_fixtures(date_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    fixtures_raw = fx_payload.get("response", [])

    aggregated: List[Dict[str, Any]] = []
    for f in fixtures_raw:
        fid = f["fixture"]["id"]           # id iz API-Football odgovora

        stats   = (await get_fixture_statistics(fid)).get("response", [])
        h2h     = (await get_head_to_head(fid)).get("response", [])
        odds    = (await get_odds(fid)).get("response", [])

        aggregated.append(
            {
                "fixture": f,       # kompletan sirovi fixture blok
                "statistics": stats,
                "h2h":        h2h,
                "odds":       odds,
            }
        )

    return aggregated
