from typing import Dict, List, Any

from AnillistPython.models import AnilistMedia
from AnillistPython.parser import parse_media


def parse_searched_media(graphql_data: Dict[str, Any]) -> List[AnilistMedia]:
    medias = graphql_data.get('media', [])
    parsed_medias = list()
    for media in medias:
        parsed_media = parse_media(media)
        if parsed_media:
            parsed_medias.append(parsed_media)

    return parsed_medias