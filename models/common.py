from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AnilistTitle:
    romaji: Optional[str] = None
    english: Optional[str] = None
    native: Optional[str] = None


@dataclass
class AnilistCharacter:
    id: int
    name: Optional[AnilistTitle] = None
    image: Optional[str] = None
    age: Optional[int] = None
    dob: Optional[datetime] = None
    description: Optional[str] = None

@dataclass
class AnilistTag:
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    is_adult: Optional[bool] = None

@dataclass
class AnilistStudio:
    id: int
    name: str

