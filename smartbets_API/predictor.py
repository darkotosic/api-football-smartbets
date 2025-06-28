# smartbets_API/predictor.py
# --------------------------------
# Integracija predikcija koristeći API-FOOTBALL podatke

import asyncio
from typing import Any, Dict, List, Optional

from .api_football import (
    get_fixtures_by_date,
    get_odds_by_fixture,
    get_team_statistics,
)

class Predictor:
    def __init__(
        self,
        league: int,
        season: int,
        bookmaker: Optional[int] = None,
    ):
        """
        :param league: ID lige koju predvidjate
        :param season: godina sezone
        :param bookmaker: opciono ID kladionice za kvote
        """
        self.league = league
        self.season = season
        self.bookmaker = bookmaker

    async def predict_fixture(
        self,
        fixture: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Predviđa ishod jedne utakmice.
        Vraća dict sa fixture_id, teams, prediction i odds.
        """
        fixture_id = fixture["fixture"]["id"]
        home = fixture["teams"]["home"]
        away = fixture["teams"]["away"]

        # Concurrentno povuci statistike i kvote
        stats_home_task = get_team_statistics(home["id"], self.league, self.season)
        stats_away_task = get_team_statistics(away["id"], self.league, self.season)
        odds_task = (
            get_odds_by_fixture(fixture_id, self.bookmaker)
            if self.bookmaker is not None
            else asyncio.sleep(0, result={"response": []})
        )

        stats_home, stats_away, odds_data = await asyncio.gather(
            stats_home_task,
            stats_away_task,
            odds_task,
        )

        resp_home = stats_home.get("response", [])[0]["league"].get("points", 0)
        resp_away = stats_away.get("response", [])[0]["league"].get("points", 0)

        # Jednostavan heuristički model: tim sa vise bodova pobeđuje, ili X
        if resp_home > resp_away:
            prediction = "1"
        elif resp_away > resp_home:
            prediction = "2"
        else:
            prediction = "X"

        return {
            "fixture_id": fixture_id,
            "teams": {"home": home, "away": away},
            "prediction": prediction,
            "odds": odds_data.get("response", []),
        }

    async def predict_by_date(
        self,
        date: str
    ) -> List[Dict[str, Any]]:
        """
        Vraća predikcije za sve utakmice na dati datum.
        date: YYYY-MM-DD
        """
        fixtures_resp = await get_fixtures_by_date(date, self.league, self.season)
        fixtures = fixtures_resp.get("response", [])
        tasks = [self.predict_fixture(f) for f in fixtures]
        return await asyncio.gather(*tasks)
