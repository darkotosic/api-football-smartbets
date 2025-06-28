import asyncio
import logging
from typing import Any, Dict, List, Optional

from .api_football import (
    get_fixtures_by_date,
    get_odds_by_fixture,
    get_team_statistics,
)

# Konfiguriši logger za debug
logger = logging.getLogger(__name__)

class Predictor:
    def __init__(
        self,
        league: int,
        season: int,
        bookmaker: Optional[int] = None,
    ):
        """
        :param league: ID lige koju predviđate
        :param season: godina sezone
        :param bookmaker: ID kladionice (opciono)
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
        Vraća dict sa fixture_id, teams, prediction i odds ili error poljem.
        """
        fixture_id = fixture.get("fixture", {}).get("id")
        home = fixture.get("teams", {}).get("home", {})
        away = fixture.get("teams", {}).get("away", {})

        try:
            # Asinhrono preuzmi statistike i kvote
            stats_home_task = get_team_statistics(
                home.get("id"), self.league, self.season
            )
            stats_away_task = get_team_statistics(
                away.get("id"), self.league, self.season
            )
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

            # Helper za bezbedno izvlačenje poena iz statistika
            def extract_points(stats: Dict[str, Any]) -> int:
                try:
                    return stats.get("response", [])[0].get("league", {}).get("points", 0)
                except Exception as exc:
                    logger.debug(f"Greška pri izvlačenju poena: {exc}")
                    return 0

            resp_home = extract_points(stats_home)
            resp_away = extract_points(stats_away)

            # Jednostavan heuristički model
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

        except Exception as exc:
            logger.error(
                f"Greška u predict_fixture za fixture {fixture_id}: {exc}",
                exc_info=True
            )
            # Vrati barem ID i poruku o grešci
            return {
                "fixture_id": fixture_id,
                "error": str(exc)
            }

    async def predict_by_date(
        self,
        date: str
    ) -> List[Dict[str, Any]]:
        """
        Vraća predikcije za sve utakmice na dati datum.
        """
        try:
            fixtures_resp = await get_fixtures_by_date(
                date,
                self.league,
                self.season
            )
            fixtures = fixtures_resp.get("response", [])
            if not fixtures:
                logger.info(
                    f"Nema utakmica za {date}, liga={self.league}, sezona={self.season}"
                )
            tasks = [self.predict_fixture(f) for f in fixtures]
            return await asyncio.gather(*tasks)

        except Exception as exc:
            logger.error(
                f"Greška u predict_by_date: {exc}",
                exc_info=True
            )
            # Propagiraj grešku dalje
            raise
