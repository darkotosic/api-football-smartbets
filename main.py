# api-football-smartbets/main.py

from dotenv import load_dotenv
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Učitaj .env
load_dotenv()

# Provera da li je API ključ postavljen
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
if not API_FOOTBALL_KEY:
    raise RuntimeError("API_FOOTBALL_KEY nije postavljen u okruženju")

app = FastAPI(
    title="API-Football Smartbets",
    version="0.2.0",
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

# Import svih rutera
from routers.countries       import router as countries_router
from routers.leagues         import router as leagues_router
from routers.teams           import router as teams_router
from routers.standings       import router as standings_router
from routers.fixtures        import router as fixtures_router
from routers.fixtures_extra  import router as fixtures_extra_router
from routers.predictions     import router as predictions_router
from routers.predictions_api import router as predictions_api_router
from routers.odds            import router as odds_router

# Registruj rutere
app.include_router(countries_router)
app.include_router(leagues_router)
app.include_router(teams_router)
app.include_router(standings_router)
app.include_router(fixtures_router)         # GET /fixtures/?...
app.include_router(fixtures_extra_router)   # /fixtures/rounds, /fixtures/head2head, itd.
app.include_router(predictions_router)      # GET /predictions/?...
app.include_router(predictions_api_router)  # GET /predictions-api/?...
app.include_router(odds_router)             # GET /odds/, /odds/mapping, /odds/bookmakers
