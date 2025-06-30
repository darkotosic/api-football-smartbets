"""
db_init.py
──────────
• kreira PostgreSQL šemu pomoću SQLAlchemy Core-a
• obuhvata: države, lige, sezone, timove, stadione, igrače (osnovno),
  mečeve (fixtures), događaje, statistiku, kvote, predikcije, tabele/standings
• čita konekcioni string iz env varijable  DATABASE_URL
"""

import os, datetime
from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, Date, DateTime, Boolean, Float, JSON,
    ForeignKey, UniqueConstraint, Index
)
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.environ["DATABASE_URL"]

engine = create_engine(DB_URL, echo=False)
meta   = MetaData(schema="public")


# ─────────────────────────── 1. STATIC / MASTER DATA ────────────────────────────
countries = Table(
    "countries", meta,
    Column("code", String(5), primary_key=True),          # "RS", "GB-ENG"…
    Column("name", String(64), nullable=False),
    Column("flag", String(256))
)

leagues = Table(
    "leagues", meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(64), nullable=False),
    Column("type", String(16)),                           # League / Cup
    Column("logo", String(256)),
    Column("country_code", String(5), ForeignKey("countries.code")),
)

seasons = Table(
    "seasons", meta,
    Column("league_id", Integer, ForeignKey("leagues.id"), primary_key=True),
    Column("year",      Integer,                          primary_key=True),
    Column("start",     Date),
    Column("end",       Date),
    Column("current",   Boolean),
)

venues = Table(
    "venues", meta,
    Column("id",      Integer, primary_key=True),
    Column("name",    String(128)),
    Column("city",    String(64)),
    Column("address", String(128)),
    Column("capacity",Integer),
    Column("surface", String(32)),
    Column("image",   String(256)),
)

teams = Table(
    "teams", meta,
    Column("id",           Integer, primary_key=True),
    Column("name",         String(64), nullable=False),
    Column("country_code", String(5), ForeignKey("countries.code")),
    Column("founded",      Integer),
    Column("logo",         String(256)),
    Column("venue_id",     Integer, ForeignKey("venues.id")),
    Index("idx_teams_name", "name")
)

players = Table(
    "players", meta,
    Column("id",        Integer, primary_key=True),
    Column("name",      String(64), nullable=False),
    Column("position",  String(16)),
    Column("nationality",String(64)),
    Column("height",    String(8)),
    Column("weight",    String(8)),
    Column("photo",     String(256)),
    Index("idx_players_name", "name")
)

# ───────────────────────────── 2. MATCH DATA ─────────────────────────────────────
fixtures = Table(
    "fixtures", meta,
    Column("id",          Integer, primary_key=True),               # fixture_id
    Column("league_id",   Integer, ForeignKey("leagues.id")),
    Column("season",      Integer),
    Column("round",       String(64)),
    Column("date_utc",    DateTime),
    Column("timestamp",   Integer),
    Column("status_long", String(32)),
    Column("status_short",String(8)),
    Column("elapsed",     Integer),
    Column("venue_id",    Integer, ForeignKey("venues.id")),
    Column("referee",     String(64)),

    Column("home_id",     Integer, ForeignKey("teams.id")),
    Column("away_id",     Integer, ForeignKey("teams.id")),
    Column("home_goals",  Integer),
    Column("away_goals",  Integer),
    Column("ht_home",     Integer),
    Column("ht_away",     Integer),
    Column("ft_home",     Integer),
    Column("ft_away",     Integer),
    Column("et_home",     Integer),
    Column("et_away",     Integer),
    Column("pen_home",    Integer),
    Column("pen_away",    Integer),

    UniqueConstraint("id", name="uq_fixtures_id")
)

fixture_statistics = Table(
    "fixture_statistics", meta,
    Column("fixture_id", Integer, ForeignKey("fixtures.id", ondelete="CASCADE"), primary_key=True),
    Column("team_id",    Integer, ForeignKey("teams.id"),          primary_key=True),
    Column("type",       String(64),                               primary_key=True),
    Column("value",      String(64)),
)

fixture_events = Table(
    "fixture_events", meta,
    Column("id",         Integer, primary_key=True, autoincrement=True),
    Column("fixture_id", Integer, ForeignKey("fixtures.id", ondelete="CASCADE")),
    Column("team_id",    Integer, ForeignKey("teams.id")),
    Column("player_id",  Integer, ForeignKey("players.id")),
    Column("assist_id",  Integer, ForeignKey("players.id")),
    Column("type",       String(32)),      # Goal / Card / Subst / VAR
    Column("detail",     String(64)),      # Yellow Card, Normal Goal…
    Column("comments",   String(128)),
    Column("elapsed",    Integer),
    Column("extra",      Integer),
)

head2head = Table(
    "head2head", meta,
    Column("id",         Integer, primary_key=True, autoincrement=True),
    Column("fixture_id", Integer, ForeignKey("fixtures.id", ondelete="CASCADE")),
    Column("data",       JSON)  # sirovi H2H JSON (fleksibilno)
)

# ──────────────────────────── 3. ODDS & BETS ─────────────────────────────────────
bookmakers = Table(
    "bookmakers", meta,
    Column("id",   Integer, primary_key=True),
    Column("name", String(64), nullable=False),
)

bets = Table(
    "bets", meta,
    Column("id",   Integer, primary_key=True),
    Column("name", String(64), nullable=False),
)

odds = Table(
    "odds", meta,
    Column("id",           Integer, primary_key=True, autoincrement=True),
    Column("fixture_id",   Integer, ForeignKey("fixtures.id", ondelete="CASCADE")),
    Column("bookmaker_id", Integer, ForeignKey("bookmakers.id")),
    Column("bet_id",       Integer, ForeignKey("bets.id")),
    Column("selection",    String(64)),      # “Over 2.5”, “Home”, …
    Column("odd",          Float),
    Column("ts_fetched",   DateTime, default=datetime.datetime.utcnow),

    UniqueConstraint("fixture_id", "bookmaker_id", "bet_id", "selection",
                     name="uq_odds_unique_line")
)

# ────────────────────────── 4. PREDICTIONS & RESULTS ─────────────────────────────
predictions = Table(
    "predictions", meta,
    Column("fixture_id",  Integer, ForeignKey("fixtures.id", ondelete="CASCADE"), primary_key=True),
    Column("model",       String(32),  primary_key=True),   # eg. btts_combo / predictor
    Column("payload",     JSON),                            # raw output modela
    Column("generated_at",DateTime, default=datetime.datetime.utcnow),
    Column("hit",         Boolean),                         # NULL dok se meč ne završi
)

# ──────────────────────────── 5. STANDINGS / TABLE ──────────────────────────────
standings = Table(
    "standings", meta,
    Column("league_id", Integer, ForeignKey("leagues.id"), primary_key=True),
    Column("season",    Integer,                           primary_key=True),
    Column("team_id",   Integer, ForeignKey("teams.id"),   primary_key=True),
    Column("rank",      Integer),
    Column("group",     String(64)),
    Column("points",    Integer),
    Column("played",    Integer),
    Column("wins",      Integer),
    Column("draws",     Integer),
    Column("losses",    Integer),
    Column("goals_for", Integer),
    Column("goals_ag",  Integer),
    Column("goals_diff",Integer),
    Column("form",      String(32)),
)

# ─────────────────────────── 6. CREATE ALL TABLES ────────────────────────────────
if __name__ == "__main__":
    print("• Kreiram šemu…")
    meta.create_all(engine, checkfirst=True)
    print("✔  Sve tabele su kreirane/već postoje.")
