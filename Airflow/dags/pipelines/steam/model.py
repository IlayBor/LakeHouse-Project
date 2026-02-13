from typing import Any, List, Optional, Annotated
from pydantic import BaseModel, Field, BeforeValidator


def validate_requirements(value: Any) -> Any:
    if value == []:
        return None
    else:
        return value


class FullGameItem(BaseModel):
    appid: int | None = None
    name: str | None = None


class Requirements(BaseModel):
    minimum: str | None = None
    recommended: str | None = None


class DemoItem(BaseModel):
    appid: int | None = None
    description: str | None = None


class PriceOverview(BaseModel):
    currency: str | None = None
    initial: float | None = None
    final: float | None = None
    discount_percent: float | None = None
    initial_formatted: str | None = None
    final_formatted: str | None = None


class PackageGroupSub(BaseModel):
    packageid: int | None = None
    percent_savings_text: str | None = None
    percent_savings: float | None = None
    option_text: str | None = None
    option_description: str | None = None
    can_get_free_license: str | None = None
    is_free_license: bool | None = None
    price_in_cents_with_discount: int | None = None


class PackageGroup(BaseModel):
    name: str | None = None
    title: str | None = None
    description: str | None = None
    selection_text: str | None = None
    save_text: str | None = None
    display_type: int | None = None
    is_recurring_subscription: str | None = None
    subs: List[PackageGroupSub] | None = None


class Platforms(BaseModel):
    windows: bool | None = None
    mac: bool | None = None
    linux: bool | None = None


class Metacritic(BaseModel):
    score: int | None = None
    url: str | None = None


class Category(BaseModel):
    id: int | None = None
    description: str | None = None


class Genre(BaseModel):
    id: str | None = None
    description: str | None = None


class Screenshot(BaseModel):
    id: int | None = None
    path_thumbnail: str | None = None
    path_full: str | None = None


class MovieResolution(BaseModel):
    resolution_480: str | None = Field(default=None, alias="480")
    max: str | None = None


class Movie(BaseModel):
    id: int | None = None
    name: str | None = None
    thumbnail: str | None = None
    webm: MovieResolution | None = None
    mp4: MovieResolution | None = None
    highlight: bool | None = None


class Recommendations(BaseModel):
    total: int | None = None


class AchievementHighlight(BaseModel):
    name: str | None = None
    path: str | None = None


class Achievements(BaseModel):
    total: int | None = None
    highlighted: List[AchievementHighlight] | None = None


class ReleaseDate(BaseModel):
    coming_soon: bool | None = None
    date: str | None = None


class SupportInfo(BaseModel):
    url: str | None = None
    email: str | None = None


class ContentDescriptors(BaseModel):
    ids: List[int] | None = None
    notes: str | None = None


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