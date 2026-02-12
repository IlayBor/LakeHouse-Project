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
    type: Optional[str] = None
    name: Optional[str] = None
    steam_appid: int
    required_age: Optional[int] = None
    is_free: Optional[bool] = None
    controller_support: Optional[str] = None
    dlc: Optional[List[int]] = None
    detailed_description: Optional[str] = None
    about_the_game: Optional[str] = None
    short_description: Optional[str] = None
    fullgame: Optional[List[FullGameItem]] = None
    supported_languages: Optional[str] = None
    header_image: Optional[str] = None
    website: Optional[str] = None
    pc_requirements: Annotated[
        Optional[Requirements], BeforeValidator(validate_requirements)
    ] = None
    mac_requirements: Annotated[
        Optional[Requirements], BeforeValidator(validate_requirements)
    ] = None
    linux_requirements: Annotated[
        Optional[Requirements], BeforeValidator(validate_requirements)
    ] = None
    legal_notice: Optional[str] = None
    developers: Optional[List[str]] = None
    publishers: Optional[List[str]] = None
    demos: Optional[List[DemoItem]] = None
    price_overview: Optional[PriceOverview] = None
    packages: Optional[List[int]] = None
    package_groups: Optional[List[PackageGroup]] = None
    platforms: Optional[Platforms] = None
    metacritic: Optional[Metacritic] = None
    categories: Optional[List[Category]] = None
    genres: Optional[List[Genre]] = None
    screenshots: Optional[List[Screenshot]] = None
    movies: Optional[List[Movie]] = None
    recommendations: Optional[Recommendations] = None
    achievements: Optional[Achievements] = None
    release_date: Optional[ReleaseDate] = None
    support_info: Optional[SupportInfo] = None
    background: Optional[str] = None
    content_descriptors: Optional[ContentDescriptors] = None
