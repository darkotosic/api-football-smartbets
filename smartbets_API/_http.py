# api-football-smartbets/smartbets_API/_http.py

import os
import httpx

# base URL for API-Football v3
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"

async def _get(endpoint: str, params: dict | None = None) -> dict:
    """
    Simple async GET wrapper.  Pulls your API key from API_FOOTBALL_KEY.
    Returns the parsed JSON payload.
    """
    headers = {
        "X-RapidAPI-Key": os.getenv("API_FOOTBALL_KEY"),
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
        r = await client.get(endpoint, params=params)
        r.raise_for_status()
        return r.json()
