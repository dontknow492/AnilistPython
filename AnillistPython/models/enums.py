from enum import Enum
from typing import Optional


class StrEnum(Enum):
    @classmethod
    def from_str(cls, value: Optional[str]):
        try:
            return cls(value) if value in cls._value2member_map_ else None
        except (TypeError, ValueError):
            return None

class MediaType(StrEnum):
    ANIME = 'ANIME'
    MANGA = 'MANGA'


class MediaFormat(StrEnum):
    TV = "TV"  # Anime broadcast on television
    TV_SHORT = "TV_SHORT"  # Under 15 minutes, TV broadcast
    MOVIE = "MOVIE"  # Theatrical release
    SPECIAL = "SPECIAL"  # DVD/Blu-ray extras, pilots, etc
    OVA = "OVA"  # Original Video Animation (DVD/Blu-ray only)
    ONA = "ONA"  # Original Net Animation (streaming)
    MUSIC = "MUSIC"  # Music videos
    MANGA = "MANGA"  # Multi-chapter manga
    NOVEL = "NOVEL"  # Light novels
    ONE_SHOT = "ONE_SHOT"  # Single-chapter manga


class MediaStatus(StrEnum):
    FINISHED = "FINISHED"  # Completed
    RELEASING = "RELEASING"  # Ongoing
    NOT_YET_RELEASED = "NOT_YET_RELEASED"  # Upcoming
    CANCELLED = "CANCELLED"  # Canceled
    HIATUS = "HIATUS"  # Temporarily paused (v2 only)


class MediaSeason(StrEnum):
    WINTER = "WINTER"  # December to February
    SPRING = "SPRING"  # March to May
    SUMMER = "SUMMER"  # June to August
    FALL = "FALL"      # September to November


class MediaSource(StrEnum):
    ORIGINAL = "ORIGINAL"               # Not based on another work
    MANGA = "MANGA"                     # Asian comic book
    LIGHT_NOVEL = "LIGHT_NOVEL"         # Written in volumes
    VISUAL_NOVEL = "VISUAL_NOVEL"       # Game with narrative focus
    VIDEO_GAME = "VIDEO_GAME"           # Generic video game
    OTHER = "OTHER"                     # Miscellaneous
    NOVEL = "NOVEL"                     # Non-volume written works
    DOUJINSHI = "DOUJINSHI"             # Self-published works
    ANIME = "ANIME"                     # Japanese anime
    WEB_NOVEL = "WEB_NOVEL"             # Online publications
    LIVE_ACTION = "LIVE_ACTION"         # Films, TV shows
    GAME = "GAME"                       # Games, not video games
    COMIC = "COMIC"                     # Comics, not manga
    MULTIMEDIA_PROJECT = "MULTIMEDIA_PROJECT"  # Mixed media
    PICTURE_BOOK = "PICTURE_BOOK"       # Illustrated books


class CharacterRole(StrEnum):
    MAIN = "MAIN"            # A primary character role in the media
    SUPPORTING = "SUPPORTING"  # A supporting character role in the media
    BACKGROUND = "BACKGROUND"  # A background character in the media


class MediaRelation(StrEnum):
    """Relations between media entries (e.g. sequel, adaptation)."""

    ADAPTATION = "ADAPTATION"
    PREQUEL = "PREQUEL"
    SEQUEL = "SEQUEL"
    PARENT = "PARENT"
    SIDE_STORY = "SIDE_STORY"
    CHARACTER = "CHARACTER"
    SUMMARY = "SUMMARY"
    ALTERNATIVE = "ALTERNATIVE"
    SPIN_OFF = "SPIN_OFF"
    OTHER = "OTHER"
    SOURCE = "SOURCE"
    COMPILATION = "COMPILATION"
    CONTAINS = "CONTAINS"


class MediaSort(Enum):
    ID = "ID"
    ID_DESC = "ID_DESC"
    TITLE_ROMAJI = "TITLE_ROMAJI"
    TITLE_ROMAJI_DESC = "TITLE_ROMAJI_DESC"
    TITLE_ENGLISH = "TITLE_ENGLISH"
    TITLE_ENGLISH_DESC = "TITLE_ENGLISH_DESC"
    TITLE_NATIVE = "TITLE_NATIVE"
    TITLE_NATIVE_DESC = "TITLE_NATIVE_DESC"
    TYPE = "TYPE"
    TYPE_DESC = "TYPE_DESC"
    FORMAT = "FORMAT"
    FORMAT_DESC = "FORMAT_DESC"
    START_DATE = "START_DATE"
    START_DATE_DESC = "START_DATE_DESC"
    END_DATE = "END_DATE"
    END_DATE_DESC = "END_DATE_DESC"
    SCORE = "SCORE"
    SCORE_DESC = "SCORE_DESC"
    POPULARITY = "POPULARITY"
    POPULARITY_DESC = "POPULARITY_DESC"
    TRENDING = "TRENDING"
    TRENDING_DESC = "TRENDING_DESC"
    EPISODES = "EPISODES"
    EPISODES_DESC = "EPISODES_DESC"
    DURATION = "DURATION"
    DURATION_DESC = "DURATION_DESC"
    STATUS = "STATUS"
    STATUS_DESC = "STATUS_DESC"
    CHAPTERS = "CHAPTERS"
    CHAPTERS_DESC = "CHAPTERS_DESC"
    VOLUMES = "VOLUMES"
    VOLUMES_DESC = "VOLUMES_DESC"
    UPDATED_AT = "UPDATED_AT"
    UPDATED_AT_DESC = "UPDATED_AT_DESC"
    SEARCH_MATCH = "SEARCH_MATCH"
    FAVOURITES = "FAVOURITES"
    FAVOURITES_DESC = "FAVOURITES_DESC"

class MediaGenre(Enum):
    ANY = "ANY"
    ACTION = "Action"
    ADVENTURE = "Adventure"
    COMEDY = "Comedy"
    DRAMA = "Drama"
    ECCHI = "Ecchi"
    FANTASY = "Fantasy"
    HENTAI = "Hentai"
    HORROR = "Horror"
    MAHOU_SHOUJO = "Mahou Shoujo"
    MECHA = "Mecha"
    MUSIC = "Music"
    MYSTERY = "Mystery"
    PSYCHOLOGICAL = "Psychological"
    ROMANCE = "Romance"
    SCI_FI = "Sci-Fi"
    SLICE_OF_LIFE = "Slice of Life"
    SPORTS = "Sports"
    SUPERNATURAL = "Supernatural"
    THRILLER = "Thriller"

if __name__ == "__main__":
    print(MediaType.from_str(MediaType.MANGA.value))