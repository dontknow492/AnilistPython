from datetime import datetime
from typing import Optional
from AnillistPython.models import AnilistCharacter
from AnillistPython.models.media import AnilistPageInfo


def parse_page_info(page_dict: dict) -> AnilistPageInfo:
    return AnilistPageInfo(
        total=page_dict.get('total', 0),
        currentPage=page_dict.get('currentPage', 1),
        lastPage=page_dict.get('lastPage', 1),
        hasNextPage=page_dict.get('hasNextPage', False),
    )

def parse_date(date_dict: Optional[dict]) -> Optional[datetime]:
    if not date_dict:
        return None
    try:
        return datetime(
            date_dict.get("year", 1),
            date_dict.get("month", 1),
            date_dict.get("day", 1)
        )
    except Exception:
        return None

def parse_character(self, character_data: dict,):
    if not character_data:
        return None
    node = character_data['node']
    return AnilistCharacter(
        id = character_data.get('id'),
        name = node.get('name', {}).get('full'),
        image = node.get('image', {}).get('large'),
        age = node.get('age', {}).get('full'),
        dob = parse_date(node.get("dateOfBirth")),
        description = node.get('description'),
    )