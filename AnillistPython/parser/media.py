import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from AnillistPython.models import  AnilistRelation, AnilistRecommendation, AnilistScore, MediaCoverImage, AnilistMediaCharacter, AnilistMedia, AnilistTitle, \
    AnilistMediaInfo, MediaFormat, MediaSource, MediaSeason, MediaStatus, MediaRelation, CharacterRole, AnilistCharacter, AnilistTag, AnilistStudio,\
    AnilistMediaBase
from AnillistPython.models.media import AnilistMediaTrailer


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

def parse_title(title_data: Optional[dict]) -> Optional['AnilistTitle']:
    if not title_data:
        return None
    return AnilistTitle(**title_data)

def parse_cover_image(img_data: Optional[dict]) -> Optional['MediaCoverImage']:
    if not img_data:
        return None
    return MediaCoverImage(
        extraLarge=img_data.get("extraLarge"),
        large=img_data.get("large"),
        medium=img_data.get("medium"),
        color=img_data.get("color")
    )


def parse_score(score_data: Optional[dict], media_id: int) -> Optional[AnilistScore]:
    if not score_data:
        return None

    return AnilistScore(
        id=media_id,
        popularity=score_data.get("popularity"),
        favourites=score_data.get("favourites"),
        average_score=score_data.get("averageScore"),
        mean_score=score_data.get("meanScore"),
    )

def parse_character(character_data: dict, media_id: int) -> Optional[AnilistMediaCharacter]:
    if not character_data:
        return None
    node = character_data['node']
    return AnilistMediaCharacter(
        id = node.get('id'),
        media_id = media_id,
        name = node.get('name', {}).get('full'),
        image = node.get('image', {}).get('large'),
        age = node.get('age'),
        dob = parse_date(node.get("dateOfBirth")),
        description = node.get('description'),
        role = CharacterRole.from_str(node.get("role")),
    )

def parse_media_info(info_data: Optional[dict], media_id: int) -> Optional[AnilistMediaInfo]:
    if not info_data:
        return None

    return AnilistMediaInfo(
        id=media_id,
        format=MediaFormat.from_str(info_data.get("format")),
        source=MediaSource.from_str(info_data.get("source")),
        country_origin=info_data.get("countryOfOrigin"),
        season=MediaSeason.from_str(info_data.get("season")),
        status=MediaStatus.from_str(info_data.get("status")),
    )

def parse_tag(tag_data: Optional[dict], media_id: int) -> Optional[AnilistTag]:
    if not tag_data:
        return None
    return AnilistTag(
        id=tag_data.get("id", media_id),
        name=tag_data.get("name"),
        description=tag_data.get("description"),
        category=tag_data.get("category"),
        is_adult=tag_data.get("isAdult")
    )

def parse_studio(studio_data: Optional[dict], media_id: int) -> Optional[AnilistStudio]:
    if not studio_data:
        return None
    node = studio_data.get('node')
    if not node:
        return None
    return AnilistStudio(
        id = node.get('id'),
        name = node.get('name'),
    )

def parse_trailer(trailer_data: Optional[dict]) -> Optional[AnilistMediaTrailer]:
    if not trailer_data:
        return None
    return AnilistMediaTrailer(
        video_id=trailer_data.get('id'),
        site = trailer_data.get('site'),
        thumbnail = trailer_data.get('thumbnail'),
    )

def parse_media_base(media_data: Dict[str, Any]) -> Optional[AnilistMediaBase]:
    media_id = media_data.get("id")  # optional fallback
    if not media_id:
        return None
    title = parse_title(media_data.get("title"))
    start_date = parse_date(media_data.get("startDate"))
    end_date = parse_date(media_data.get("endDate"))
    image = parse_cover_image(media_data.get("coverImage"))

    info = parse_media_info(media_data, media_id)
    score = parse_score(media_data, media_id)

    characters = media_data.get("characters")
    tags = media_data.get("tags")
    studios = media_data.get("studios")
    character_list = []
    tag_list = []
    studio_list = []
    if characters:
        for character in characters.get("edges", []):
            character_data = parse_character(character, media_id)
            if character_data:
                character_list.append(character_data)
    if tags:
        for tag in tags:
            tag_data = parse_tag(tag, media_id)
            if tag_data:
                tag_list.append(tag_data)

    if studios:
        for studio in studios.get("edges", []):
            studio_data = parse_studio(studio, media_id)
            if data:
                studio_list.append(studio_data)

    return AnilistMediaBase(
        id=media_id,
        idMal = media_data.get("idMal"),
        title=title,
        cover_image=image,
        description=media_data.get("description"),
        genres=media_data.get("genres"),
        score=score,
        info=info,
        synonyms=media_data.get("synonyms"),
        tags=tag_list,
        start_date=start_date,
        end_date=end_date,
        studios=studio_list,
        characters=character_list,
        trailer=parse_trailer(media_data.get("trailer")),
        site_url=media_data.get("siteUrl"),
        isAdult=media_data.get("isAdult"),
        duration=media_data.get("duration"),
        episodes=media_data.get("episodes"),
        chapters=media_data.get("chapters"),
        volumes=media_data.get("volumes"),
    )

def parse_relation(relation_data: Optional[dict], media_id: int) -> Optional['AnilistRelation']:
    """
    :param relation_data: value at data[AnilistMedia][relation][edges][index]
    :param media_id: id of media
    :return:
    """
    if not relation_data:
        return None
    node = relation_data.get('node')
    relation_type = relation_data.get("relationType")
    return AnilistRelation(
        from_media_id=media_id,  # Set to 0 or update dynamically if you track current media id
        relation_type=MediaRelation.from_str(relation_type),
        media=parse_media_base(node)
    )

def parse_recommendation(media_id: int, media_data: Dict[str, Any] ) -> Optional[AnilistRecommendation]:
    """
    :param media_id: id of media
    :param media_data: value at data[AnilistMedia][recommendations][nodes][mediaRecommendation]
    :return: data class of AnilistRecommendation
    """
    if not media_data:
        return None

    return AnilistRecommendation(
        from_media_id=media_id,
        media=parse_media_base(media_data)
    )

def parse_media(media_data: dict) -> Optional[AnilistMedia]:
    media_id = media_data.get("id")  # optional fallback
    if not media_id:
        return None

    media = parse_media_base(media_data)



    relations = media_data.get("relations")
    recommendations = media_data.get("recommendations")

    relation_list = []
    recommendation_list = []

    if relations:
        for relation in relations.get("edges", []):
            rel_data = parse_relation(relation, media_id)
            if rel_data:
                relation_list.append(rel_data)
    if recommendations:
        for recommendation in recommendations.get("nodes", []):
            recom_data = parse_recommendation(media_id, recommendation.get("mediaRecommendation"))
            if recom_data:
                recommendation_list.append(recom_data)

    return AnilistMedia(
        **vars(media),
        relations=relation_list,
        recommendations=recommendation_list
    )

def parse_graphql_media_data(graphql_media_data: Dict[str, Any]) -> Optional[AnilistMedia]:
    media_data = graphql_media_data.get("data", {}).get("AnilistMedia")
    if not media_data:
        print("'AnilistMedia' not found trying to fetch 'media'")
        media_data = graphql_media_data.get("data", {}).get("media")
    if not media_data:
        print("media data is empty")
        return None

    return parse_media(media_data)

if __name__ == '__main__':
    from pprint import pprint
    import json
    path = Path(r"D:\Program\AnilistPython\samples\media_2.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    media_data = data["data"]["media"]
    # print(data.keys())
    media = parse_media(media_data)
    pprint(media)