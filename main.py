# api-football-smartbets/main.py

from dotenv import load_dotenv
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.countries      import router as countries_router
from routers.leagues        import router as leagues_router
from routers.teams          import router as teams_router
from routers.standings      import router as standings_router
from routers.fixtures_extra import router as fixtures_router
from routers.predictions    import router as predictions_router
from routers.predictions_api import router as predictions_api_router
from routers.odds           import router as odds_router
from routers.today          import router as today_router

# load .env
load_dotenv()
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
if not API_FOOTBALL_KEY:
    raise RuntimeError("API_FOOTBALL_KEY not set in environment")

app = FastAPI(
    title="API-Football Smartbets",
    version="0.2.0",
    description="FastAPI service for predictions and API-Football data"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # in prod tighten this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register all routers
app.include_router(countries_router)
app.include_router(leagues_router)
app.include_router(teams_router)
app.include_router(standings_router)
app.include_router(fixtures_router)
app.include_router(predictions_router)
app.include_router(predictions_api_router)
app.include_router(odds_router)
app.include_router(today_router)
