from typing import List, Optional
from pydantic import BaseModel, Field

class TeamInfo(BaseModel):
    id: int
    name: str
    logo: Optional[str]
    winner: Optional[bool]

class FixtureInfo(BaseModel):
    id: int = Field(..., alias='fixture_id')
    date: str
    venue: Optional[dict]
    status: Optional[dict]
    teams: dict

class OddsInfo(BaseModel):
    bookmaker: Optional[int]
    bets: Optional[List[dict]]

class PredictionResponse(BaseModel):
    fixture_id: int
    teams: dict
    prediction: str
    odds: List[dict]
    error: Optional[str] = None