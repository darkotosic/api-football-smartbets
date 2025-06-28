# API-Football Smartbets

**FastAPI servis za predikcije i podatke iz API-Football v3**

---

## Pregled

Ovaj projekat je REST API izgrađen pomoću FastAPI-a koji obezbeđuje pristup raznovrsnim podacima iz [API-Football v3](https://www.api-football.com/):

* **Countries** ( `/countries/`)
* **Leagues** ( `/leagues/` i `/leagues/{league_id}/seasons`)
* **Teams** ( `/teams/` i `/teams/{team_id}/statistics`)
* **Standings** ( `/standings/`)
* **Fixtures** ( `/fixtures/`, `/fixtures/rounds`, `/fixtures/head2head`, `/fixtures/{id}/statistics`, `/fixtures/{id}/events`)
* **Predictions** ( `/predictions/` i `/predictions-api/`)
* **Odds (Pre-Match)** ( `/odds/`, `/odds/mapping`, `/odds/bookmakers`)

Svaki endpoint vraća čist JSON niz objekata (pomoću Pydantic modela iz `models.py`).

---

## Quickstart

### 1. Kloniraj repo

```bash
git clone https://github.com/darkotosic/api-football-smartbets.git
cd api-football-smartbets
```

### 2. Kreiraj virtuelno okruženje i instaliraj zavisnosti

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.\.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Postavi API ključ

Kreiraj fajl `.env` u korenu projekta:

```
API_FOOTBALL_KEY=YOUR_API_FOOTBALL_KEY_HERE
```

### 4. Pokreni server

```bash
uvicorn main:app --reload
```

Otvorite [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) za Swagger UI.

---

## Primeri upotrebe

#### Dohvati sve države

```bash
curl -X GET "http://127.0.0.1:8000/countries/" -H "accept: application/json"
```

#### Dohvati lige po državi

```bash
curl "http://127.0.0.1:8000/leagues/?country=England"
```

#### Dohvati sezone za ligu

```bash
curl "http://127.0.0.1:8000/leagues/39/seasons"
```

#### Dohvati timove u ligi i sezoni

```bash
curl "http://127.0.0.1:8000/teams/?league=39&season=2025"
```

#### Dohvati plasman (standings)

```bash
curl "http://127.0.0.1:8000/standings/?league=39&season=2025"
```

#### Dohvati utakmice za datum

```bash
curl "http://127.0.0.1:8000/fixtures/?date=2025-06-28&league=39&season=2025"
```

#### Dohvati head-to-head statistiku

```bash
curl "http://127.0.0.1:8000/fixtures/head2head?team1=40&team2=41&season=2025"
```

#### Dohvati predikcije (API-Football)

```bash
curl "http://127.0.0.1:8000/predictions-api/?fixture=123456&bookmaker=8"
```

#### Dohvati kvote pre-match

```bash
curl "http://127.0.0.1:8000/odds/?fixture=123456&bookmaker=8"
```

---

## Razvoj i doprinos

1. Preuzmi projekat i kreiraj novu granu:

   ```bash
   ```

git checkout -b feature/moja-nova-funkcija

```
2. Dodaj izmene, napiši testove u `tests/`
3. Pošalji Pull Request

---

## Preporuke za dalje

- **Pydantic modeli**: u `models.py` definiši `Country`, `League`, `Team`, `Fixture`, `Prediction`, `Odds` itd.
- **Testovi**: dodaj `pytest` testove u `tests/` folder. Pokreni `pytest` pre svakog commita.
- **Docker**: napiši `Dockerfile` i `docker-compose.yml` za lako deploy-ovanje.
- **Cache / rate limiting**: implementiraj `fastapi-cache` ili Redis TTL za zahtevne rute.
- **Error handling**: koristi specifične `HTTPException(status_code=...)` i loguj greške.

---

© 2025 darkotosic – Open‑source (MIT)

```
