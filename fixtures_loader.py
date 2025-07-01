#!/usr/bin/env python
"""
fixtures_loader.py

▲ Što radi?
    • dohvaća fixtur(e) za zadani datum  (default = danas, UTC)
    • popunjava / ažurira tablicu  fixtures  u Postgres bazi
    • pokreće se ručno:        python fixtures_loader.py 2025-07-01
      ili iz Cron job-a / Background Worker-a bez argumenata

▲ Zahtjevi:
    • varijabla okoline  DATABASE_URL   (Postgres konekcija)
    • API ključ je već u  API_FOOTBALL_KEY  i koristi se u wrapperu
    • SQLAlchemy 2.x +  psycopg2-binary  (u requirements.txt)
"""

import os
import sys
import datetime as dt
from typing import List

from sqlalchemy import create_engine, MetaData
from sqlalchemy.dialects.postgresql import insert as pg_insert

# tvoj wrapper
from smartbets_API.api_football import get_fixtures_by_date


def _iso_date(arg: str | None) -> dt.date:
    """vrati date objekt iz YYYY-MM-DD stringa ili današnji datum."""
    if arg:
        return dt.date.fromisoformat(arg)
    return dt.datetime.utcnow().date()


def _flatten_fixture(raw: dict) -> dict:
    """
    Iz raw JSON-a (kakav vraća api_football) izvlači kolone
    koje postoje u tablici  fixtures.
    Prilagodi nazive ako si u DB shemi drugačije imenovao!
    """
    fxt   = raw["fixture"]["fixture"]
    lg    = raw["fixture"]["league"]
    teams = raw["fixture"]["teams"]
    goals = raw["fixture"]["goals"]
    stat  = fxt["status"]

    return {
        "fixture_id":      fxt["id"],

        # FK prema leagues / teams (već moraju postojati ili radi ON CONFLICT … NOTHING)
        "league_id":       lg["id"],
        "season":          lg["season"],
        "home_team_id":    teams["home"]["id"],
        "away_team_id":    teams["away"]["id"],

        # osnovni podaci
        "date_utc":        fxt["date"],       # ISO string
        "timestamp":       fxt["timestamp"],  # epoch (int)
        "venue_name":      fxt["venue"]["name"] if fxt["venue"] else None,
        "venue_city":      fxt["venue"]["city"] if fxt["venue"] else None,

        # status + rezultat
        "status_short":    stat["short"],
        "status_long":     stat["long"],
        "elapsed":         stat["elapsed"],

        "goals_home":      goals["home"],
        "goals_away":      goals["away"],
    }


def save_fixtures(rows: List[dict]) -> None:
    """
    Bulk upsert u Postgres.
    Ako već postoji isti fixture_id → UPDATE svih ostalih kolona.
    """
    db_url = os.environ["DATABASE_URL"]
    engine = create_engine(db_url, pool_pre_ping=True)

    meta = MetaData()
    meta.reflect(bind=engine, only=("fixtures",))
    fixtures_t = meta.tables["fixtures"]

    with engine.begin() as conn:
        stmt = pg_insert(fixtures_t).values(rows)
        # sve kolone osim PK (fixture_id) update-amo kada se sudare
        update_cols = {c: stmt.excluded[c]
                       for c in rows[0].keys() if c != "fixture_id"}
        stmt = stmt.on_conflict_do_update(
            index_elements=["fixture_id"],
            set_=update_cols
        )
        conn.execute(stmt)


def main(argv: list[str]) -> None:
    target_date = _iso_date(argv[1] if len(argv) > 1 else None)
    print(f"➡️  Povlačim fixtur(e) za {target_date.isoformat()} …")

    raw_fixtures = get_fixtures_by_date(target_date.isoformat())

    if not raw_fixtures:
        print("⚠️  Nema fixtura za taj datum.")
        return

    rows = [_flatten_fixture(item) for item in raw_fixtures]
    save_fixtures(rows)
    print(f"✓ U bazi upisano / ažurirano {len(rows)} fixtura.")


if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as exc:       # noqa: BLE001
        # Grešku ispiši da bude vidljiva u Render log-ovima
        import traceback
        traceback.print_exc()
        sys.exit(1)
