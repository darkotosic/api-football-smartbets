# api-football-smartbets/models.py

from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


# ── 1. COUNTRIES ─────────────────────────────────────────────────────────────────

class Country(BaseModel):
    name: str
    code: Optional[str]
    flag: Optional[str]


# ── 2. LEAGUES ────────────────────────────────────────────────────────────────────

class League(BaseModel):
    id: int
    name: str
    country: str
    logo: Optional[str]
    flag: Optional[str]


class LeagueSeasonList(BaseModel):
    league: League
    seasons: List[int]


# ── 3. TEAMS ──────────────────────────────────────────────────────────────────────

class Team(BaseModel):
    id: int
    name: str
    logo: Optional[str]


class TeamStatistics(BaseModel):
    team: Team
    statistics: Dict[str, Any]  # možeš razraditi na konkretna polja po potrebi


# ── 4. STANDINGS ─────────────────────────────────────────────────────────────────

class StandingEntry(BaseModel):
    rank: int
    team: Team
    points: int
    goalsDiff: int
    played: int
    form: Optional[str]
    group: Optional[str]
    description: Optional[str]


class StandingsResponse(BaseModel):
    league: League
    standings: List[StandingEntry]


# ── 5. FIXTURES ──────────────────────────────────────────────────────────────────

class FixtureInfo(BaseModel):
    id: int
    referee: Optional[str]
    timezone: str
    date: str
    timestamp: int


class Venue(BaseModel):
    id: int
    name: str
    city: Optional[str]


class FixtureStatus(BaseModel):
    long: str
    short: str
    elapsed: Optional[int]
    extra: Optional[int]


class FixtureTeams(BaseModel):
    home: Team
    away: Team


class Fixture(BaseModel):
    fixture: FixtureInfo
    league: League
    teams: FixtureTeams
    venue: Venue
    status: FixtureStatus
    goals: Optional[Dict[str, Optional[int]]]


# ── 6. FIXTURE EXTRA (ROUNDS / H2H / STATS / EVENTS) ──────────────────────────────

class Round(BaseModel):
    round: str
    start: str
    end: str


class Head2HeadEntry(BaseModel):
    fixture: FixtureInfo
    teams: FixtureTeams
    score: Dict[str, Any]


class FixtureStatistic(BaseModel):
    team: Team
    statistics: Dict[str, Any]


class FixtureEvent(BaseModel):
    time: Dict[str, Any]
    team: Team
    player: Dict[str, Any]
    type: str
    detail: str


# ── 7. PREDICTIONS ─────────────────────────────────────────────────────────────────

class PredictionResponse(BaseModel):
    fixture_id: int
    teams: FixtureTeams
    prediction: str
    odds: List[Dict[str, Any]]
    error: Optional[str]


# ── 8. ODDS (PRE-MATCH) ───────────────────────────────────────────────────────────

class Bookmaker(BaseModel):
    id: int
    name: str
    bets: List[Dict[str, Any]]


class OddsMappingEntry(BaseModel):
    odd: str
    value: str


class OddsResponse(BaseModel):
    league: League
    fixture: FixtureInfo
    bookmaker: Bookmaker
    bets: List[OddsMappingEntry]


# ── 9. GENERIČKI TYPING ZA NEPOZNATA POLJA ─────────────────────────────────────────

JSONDict = Dict[str, Any]
