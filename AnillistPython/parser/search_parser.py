from typing import Dict, List, Any, Set, Optional

from AnillistPython.models import AnilistMedia, MediaType
from AnillistPython.parser import parse_media


def parse_searched_media(graphql_data: Dict[str, Any], media_type: MediaType,
                         media_fields: Optional[Set[str]] = None, relations_fields: Optional[Set[str]] = None,
                         recommendation_fields: Optional[Set[str]] = None) -> List[AnilistMedia]:
    graphql_data = graphql_data["Page"]
    medias = graphql_data.get('media', [])
    parsed_medias = list()
    for media in medias:
        parsed_media = parse_media(media, media_type, media_fields, relations_fields, recommendation_fields)
        if parsed_media:
            parsed_medias.append(parsed_media)

    return parsed_medias