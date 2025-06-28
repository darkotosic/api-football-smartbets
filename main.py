# api-football-smartbets/main.py

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from smartbets_API.api_football import (
    get_fixtures_by_date,
)
from smartbets_API.predictor import Predictor

# Učitavanje ENV
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
if not API_FOOTBALL_KEY:
    raise RuntimeError("API_FOOTBALL_KEY nije postavljen u okruženju")

app = FastAPI(
    title="API-Football Smartbets",
    version="0.1.0",
    description="FastAPI servis za predikcije i podatke iz API-Football"
)

# CORS (za razvoj dozvoli sve origin; u produkciji suzi domene)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/fixtures/")
async def fixtures(
    date: str,
    league: Optional[int] = None,
    season: Optional[int] = None
):
    """
    Vraća listu utakmica (fixtures) za zadati datum.
    query params:
      - date: YYYY-MM-DD
      - league: opcioni ID lige
      - season: opcioni sezon (npr. 2025)
    """
    try:
        data = await get_fixtures_by_date(date, league, season)
        return data.get("response", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predictions/")
async def predictions(
    date: str,
    league: int,
    season: int,
    bookmaker: Optional[int] = None
):
    """
    Vraća predikcije za sve utakmice tog datuma.
    query params:
      - date: YYYY-MM-DD
      - league: ID lige (obavezno)
      - season: godina sezone (obavezno)
      - bookmaker: opcioni ID kladionice
    """
    try:
        predictor = Predictor(league=league, season=season, bookmaker=bookmaker)
        results = await predictor.predict_by_date(date)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
