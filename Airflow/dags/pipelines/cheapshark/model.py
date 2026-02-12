from typing import Any, List, Optional, Annotated
from datetime import date
from pydantic import BaseModel, Field


class GameDeal(BaseModel):
    internalName: str
    title: str
    metacriticLink: str | None
    dealID: str
    storeID: str
    gameID: str
    salePrice: float
    normalPrice: float
    isOnSale: bool
    savings: float
    metacriticScore: int
    steamRatingText: str | None = None
    steamRatingPercent: Optional[int] = None
    steamRatingCount: Optional[int] = None
    steamAppID: Optional[str] = None
    releaseDate: int
    lastChange: int
    dealRating: float
    thumb: str
    ingestionDate: Optional[date] = Field(default_factory=date.today)
