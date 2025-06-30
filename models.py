# api-football-smartbets/models.py

from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class CustomBaseModel(BaseModel):
    """
    Base for all our models:
    - ignore extra fields from API
    - allow population by alias
    """
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

# 1. COUNTRY
class Country(CustomBaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    flag: Optional[str] = None

# 2. LEAGUE
class League(CustomBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    country: Optional[str] = None
    logo: Optional[str] = None
    flag: Optional[str] = None

class LeagueSeasonList(CustomBaseModel):
    league: League = Field(default_factory=League)
    seasons: List[int] = Field(default_factory=list)

# 3. TEAM
class Team(CustomBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    logo: Optional[str] = None

class TeamStatistics(CustomBaseModel):
    team: Team = Field(default_factory=Team)
    statistics: Dict[str, Any] = Field(default_factory=dict)

# 4. STANDINGS
class StandingEntry(CustomBaseModel):
    rank: Optional[int] = None
    team: Team = Field(default_factory=Team)
    points: Optional[int] = None
    goalsDiff: Optional[int] = None
    played: Optional[int] = None
    form: Optional[str] = None
    group: Optional[str] = None
    description: Optional[str] = None
    all: Dict[str, Any] = Field(default_factory=dict)

# 5. FIXTURES
class FixtureInfo(CustomBaseModel):
    id: Optional[int] = Field(None, alias="fixture_id")
    referee: Optional[str] = None
    timezone: Optional[str] = None
    date: Optional[str] = None
    timestamp: Optional[int] = None

class Venue(CustomBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    city: Optional[str] = None

class FixtureStatus(CustomBaseModel):
    long: Optional[str] = None
    short: Optional[str] = None
    elapsed: Optional[int] = None
    extra: Optional[int] = None

class FixtureTeams(CustomBaseModel):
    home: Team = Field(default_factory=Team)
    away: Team = Field(default_factory=Team)

class Fixture(CustomBaseModel):
    fixture: FixtureInfo = Field(default_factory=FixtureInfo)
    league: League = Field(default_factory=League)
    teams: FixtureTeams = Field(default_factory=FixtureTeams)
    venue: Venue = Field(default_factory=Venue)
    status: FixtureStatus = Field(default_factory=FixtureStatus)
    goals: Dict[str, Optional[int]] = Field(default_factory=dict)

# 6. HEAD-TO-HEAD & STATS & EVENTS
class Head2HeadEntry(CustomBaseModel):
    fixture: FixtureInfo = Field(default_factory=FixtureInfo)
    teams: FixtureTeams = Field(default_factory=FixtureTeams)
    score: Dict[str, Any] = Field(default_factory=dict)

class FixtureStatistic(CustomBaseModel):
    team: Team = Field(default_factory=Team)
    statistics: Dict[str, Any] = Field(default_factory=dict)

class FixtureEvent(CustomBaseModel):
    time: Dict[str, Any] = Field(default_factory=dict)
    team: Team = Field(default_factory=Team)
    player: Dict[str, Any] = Field(default_factory=dict)
    type: Optional[str] = None
    detail: Optional[str] = None

# 7. PREDICTIONS
class PredictionResponse(CustomBaseModel):
    fixture_id: Optional[int] = None
    teams: FixtureTeams = Field(default_factory=FixtureTeams)
    prediction: Optional[str] = None
    odds: List[Dict[str, Any]] = Field(default_factory=list)
    error: Optional[str] = None

class APIPrediction(CustomBaseModel):
    league: League = Field(default_factory=League)
    teams: FixtureTeams = Field(default_factory=FixtureTeams)
    predictions: Dict[str, Any] = Field(default_factory=dict)

# 8. ODDS
class OddsMappingEntry(CustomBaseModel):
    odd: Optional[str] = None
    value: Optional[str] = None

class BookmakerInfo(CustomBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    bets: List[Dict[str, Any]] = Field(default_factory=list)

class OddsResponse(CustomBaseModel):
    league: League = Field(default_factory=League)
    fixture: FixtureInfo = Field(default_factory=FixtureInfo)
    bookmaker: BookmakerInfo = Field(default_factory=BookmakerInfo)
    bets: List[OddsMappingEntry] = Field(default_factory=list)

# 9. TODAY AGGREGATE
class TodayFixtureData(CustomBaseModel):
    fixture: Fixture = Field(default_factory=Fixture)
    odds: List[OddsResponse] = Field(default_factory=list)
    h2h: List[Head2HeadEntry] = Field(default_factory=list)
    prediction: Optional[PredictionResponse] = None
