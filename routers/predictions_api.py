from fastapi import APIRouter
from typing import List, Optional
from smartbets_API.api_football import get_api_predictions

router = APIRouter(prefix="/predictions-api", tags=["predictions-api"])

@router.get("/", response_model=List[dict])
async def read_api_predictions(
    fixture: int,
    bookmaker: Optional[int] = None
):
    data = await get_api_predictions(fixture, bookmaker)
    return data.get("response", [])
