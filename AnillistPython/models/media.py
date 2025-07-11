from datetime import datetime
from enum import Enum
from typing import Optional, List

from AnillistPython.models.common import AnilistTitle, AnilistTag, AnilistStudio, AnilistCharacter
from AnillistPython.models.enums import (MediaType, MediaFormat, MediaSeason, MediaSource, MediaStatus, CharacterRole,
                                         MediaGenre, MediaRelation)
from dataclasses import dataclass


@dataclass
class MediaCoverImage:
    """
    The cover image url of the media at its largest size. If this size isn't available, large will be provided instead.
    """
    extraLarge: Optional[str] = None

    """The cover image url of the media at a large size"""
    large: Optional[str] = None

    """The cover image url of the media at medium size"""
    medium: Optional[str] = None

    """Average #hex color of cover image"""
    color: Optional[str] = None



@dataclass
class AnilistScore:
    id: int #media id
    popularity: Optional[int] = None
    favourites: Optional[int] = None
    average_score: Optional[int] = None
    mean_score: Optional[int] = None

@dataclass
class AnilistMediaInfo:
    id: int #media id
    format: Optional[MediaFormat] = None
    source: Optional[MediaSource] = None
    country_origin: Optional[str] = None
    season: Optional[MediaSeason] = None
    status: Optional[MediaStatus] = None

@dataclass
class AnilistMediaCharacter(AnilistCharacter):
    media_id: int = None
    role: Optional[CharacterRole] = None


@dataclass
class AnilistMediaTrailer:
    video_id: str = None
    site: Optional[str] = None
    thumbnail: Optional[str] = None

@dataclass
class AnilistMediaBase:
    id: int
    title: Optional[AnilistTitle] = None
    description: Optional[str] = None
    coverImage: Optional[MediaCoverImage] = None
    bannerImage: Optional[str] = None
    synonyms: Optional[List[str]] = None

    tags: Optional[List[AnilistTag]] = None
    genres: Optional[List[MediaGenre]] = None
    studios: Optional[List[AnilistStudio]] = None

    score: Optional[AnilistScore] = None

    info: Optional[AnilistMediaInfo] = None

    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None

    characters: Optional[List[AnilistCharacter]] = None

    duration: Optional[int] = None
    episodes: Optional[int] = None

    chapters: Optional[int] = None
    volumes: Optional[int] = None

    isAdult: Optional[bool] = None
    trailer: Optional[AnilistMediaTrailer] = None
    siteUrl: Optional[str] = None
    idMal: Optional[int] = None
    # todo: update query builder, parser for bellow data
    media_type: Optional[MediaType] = None,

    next_episode: Optional[int] = None,
    next_episode_airing_at: Optional[int] = None,
    time_until_next_episode: Optional[int] = None


@dataclass
class AnilistRelation:
    from_media_id: int  # current media
    relation_type: Optional[MediaRelation] = None  # e.g. PREQUEL, SEQUEL
    media: Optional[AnilistMediaBase] = None


@dataclass
class AnilistRecommendation:
    from_media_id: int
    media: Optional[AnilistMediaBase] = None

@dataclass
class AnilistMedia(AnilistMediaBase):
    relations: Optional[List[AnilistRelation]] = None
    recommendations: Optional[List[AnilistRecommendation]] = None

@dataclass
class AnilistEpisode:
    media_id: id
    title: str
    thumbnail: str
    official_url: str
    official_site: str

@dataclass
class AnilistPageInfo:
    total: int
    currentPage: int
    lastPage: int
    hasNextPage: bool

@dataclass
class AnilistSearchResult:
    pageInfo: AnilistPageInfo
    medias: List[AnilistMedia]