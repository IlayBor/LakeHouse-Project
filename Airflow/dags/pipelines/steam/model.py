from typing import Any, List, Optional, Annotated
from pydantic import BaseModel, Field, BeforeValidator


def validate_requirements(value: Any) -> Any:
    if value == []:
        return None
    else:
        return value


class FullGameItem(BaseModel):
    appid: Optional[int] = None
    name: Optional[str] = None


class Requirements(BaseModel):
    minimum: Optional[str] = None
    recommended: Optional[str] = None


class DemoItem(BaseModel):
    appid: Optional[int] = None
    description: Optional[str] = None


class PriceOverview(BaseModel):
    currency: Optional[str] = None
    initial: Optional[float] = None
    final: Optional[float] = None
    discount_percent: Optional[float] = None
    initial_formatted: Optional[str] = None
    final_formatted: Optional[str] = None


class PackageGroupSub(BaseModel):
    packageid: Optional[int] = None
    percent_savings_text: Optional[str] = None
    percent_savings: Optional[float] = None
    option_text: Optional[str] = None
    option_description: Optional[str] = None
    can_get_free_license: Optional[str] = None
    is_free_license: Optional[bool] = None
    price_in_cents_with_discount: Optional[int] = None


class PackageGroup(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    selection_text: Optional[str] = None
    save_text: Optional[str] = None
    display_type: Optional[int] = None
    is_recurring_subscription: Optional[str] = None
    subs: Optional[List[PackageGroupSub]] = None


class Platforms(BaseModel):
    windows: Optional[bool] = None
    mac: Optional[bool] = None
    linux: Optional[bool] = None


class Metacritic(BaseModel):
    score: Optional[int] = None
    url: Optional[str] = None


class Category(BaseModel):
    id: Optional[int] = None
    description: Optional[str] = None


class Genre(BaseModel):
    id: Optional[str] = None
    description: Optional[str] = None


class Screenshot(BaseModel):
    id: Optional[int] = None
    path_thumbnail: Optional[str] = None
    path_full: Optional[str] = None


class MovieResolution(BaseModel):
    resolution_480: Optional[str] = Field(default=None, alias="480")
    max: Optional[str] = None


class Movie(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    thumbnail: Optional[str] = None
    webm: Optional[MovieResolution] = None
    mp4: Optional[MovieResolution] = None
    highlight: Optional[bool] = None


class Recommendations(BaseModel):
    total: Optional[int] = None


class AchievementHighlight(BaseModel):
    name: Optional[str] = None
    path: Optional[str] = None


class Achievements(BaseModel):
    total: Optional[int] = None
    highlighted: Optional[List[AchievementHighlight]] = None


class ReleaseDate(BaseModel):
    coming_soon: Optional[bool] = None
    date: Optional[str] = None


class SupportInfo(BaseModel):
    url: Optional[str] = None
    email: Optional[str] = None


class ContentDescriptors(BaseModel):
    ids: Optional[List[int]] = None
    notes: Optional[str] = None


class SteamGame(BaseModel):
    type: str | None = None
    name: str | None = None
    steam_appid: int
    required_age: int | None = None
    is_free: bool | None = None
    controller_support: str | None = None
    dlc: List[int] | None = None
    detailed_description: str | None = None
    about_the_game: str | None = None
    short_description: str | None = None
    fullgame: List[FullGameItem] | None = None
    supported_languages: str | None = None
    header_image: str | None = None
    website: str | None = None
    pc_requirements: Annotated[
        Requirements | None, BeforeValidator(validate_requirements)
    ] = None
    mac_requirements: Annotated[
        Requirements | None, BeforeValidator(validate_requirements)
    ] = None
    linux_requirements: Annotated[
        Requirements | None, BeforeValidator(validate_requirements)
    ] = None
    legal_notice: str | None = None
    developers: List[str] | None = None
    publishers: List[str] | None = None
    demos: List[DemoItem] | None = None
    price_overview: PriceOverview | None = None
    packages: List[int] | None = None
    package_groups: List[PackageGroup] | None = None
    platforms: Platforms | None = None
    metacritic: Metacritic | None = None
    categories: List[Category] | None = None
    genres: List[Genre] | None = None
    screenshots: List[Screenshot] | None = None
    movies: List[Movie] | None = None
    recommendations: Recommendations | None = None
    achievements: Achievements | None = None
    release_date: ReleaseDate | None = None
    support_info: SupportInfo | None = None
    background: str | None = None
    content_descriptors: ContentDescriptors | None = None
