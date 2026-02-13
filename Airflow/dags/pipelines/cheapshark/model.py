from typing import Any, List, Optional, Annotated
from datetime import date
from pydantic import BaseModel, Field


class GameDeal(BaseModel):
    internalName: str | None = None
    title: str | None = None
    metacriticLink: str | None = None
    dealID: str
    storeID: str | None = None
    gameID: str | None = None
    salePrice: float | None = None
    normalPrice: float | None = None
    isOnSale: bool | None = None
    savings: float | None = None
    metacriticScore: int | None = None
    steamRatingText: str | None = None
    steamRatingPercent: int | None = None
    steamRatingCount: int | None = None
    steamAppID: str | None = None
    releaseDate: int | None = None
    lastChange: int | None = None
    dealRating: float | None = None
    thumb: str | None = None
    ingestionDate: date = Field(default_factory=date.today)
