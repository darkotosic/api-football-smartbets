# models.py
from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Country(BaseModel):
    name: str
    code: Optional[str]
    flag: Optional[str]

class League(BaseModel):
    id: int
    name: str
    country: str
    logo: Optional[str]
    flag: Optional[str]

class LeagueSeasonList(BaseModel):
    league: League
    seasons: List[int]

class Team(BaseModel):
    id: int
    name: str
    logo: Optional[str]

class TeamStatistics(BaseModel):
    team: Team
    statistics: Dict[str, Any]

class StandingEntry(BaseModel):
    rank: int
    team: Team
    points: int
    goalsDiff: int
    played: int
    form: Optional[str]
    group: Optional[str]
    description: Optional[str]

class FixtureInfo(BaseModel):
    id: int = Field(..., alias="fixture_id")
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

class Head2HeadEntry(BaseModel):
    fixture: FixtureInfo
    teams: FixtureTeams
    score: Dict[str, Any]

class FixtureStatistic(BaseModel):
    team: Team
    statistics: Dict[str, Any]

class OddsMappingEntry(BaseModel):
    odd: Optional[str]
    value: Optional[str]

class BookmakerInfo(BaseModel):
    id: Optional[int]
    name: Optional[str]
    bets: List[Dict[str, Any]] = Field(default_factory=list)

class OddsResponse(BaseModel):
    league: League
    fixture: FixtureInfo
    bookmaker: BookmakerInfo
    bets: List[OddsMappingEntry]

class TodayFixtureData(BaseModel):
    fixture: Fixture
    statistics: List[FixtureStatistic]
    h2h: List[Head2HeadEntry]
    odds: List[OddsResponse]
