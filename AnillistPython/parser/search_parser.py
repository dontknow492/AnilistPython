from typing import Dict, List, Any, Set, Optional

from AnillistPython.models import AnilistMedia, MediaType, AnilistSearchResult
from AnillistPython.parser.common import parse_page_info
from AnillistPython.parser.media import parse_media


def parse_searched_media(graphql_data: Dict[str, Any], media_type: MediaType,
                         media_fields: Optional[Set[str]] = None, relations_fields: Optional[Set[str]] = None,
                         recommendation_fields: Optional[Set[str]] = None) -> AnilistSearchResult:
    graphql_data = graphql_data["Page"]
    page_info = graphql_data["pageInfo"]
    medias = graphql_data.get('media', [])
    parsed_medias = list()
    for media in medias:
        parsed_media = parse_media(media, media_type, media_fields, relations_fields, recommendation_fields)
        if parsed_media:
            parsed_medias.append(parsed_media)

    page_info = parse_page_info(page_info)

    search_result = AnilistSearchResult(page_info, parsed_medias)

    return search_result