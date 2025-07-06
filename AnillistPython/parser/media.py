import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Set, List

# from AnillistPython import MediaGenre
from AnillistPython.models import  AnilistRelation, AnilistRecommendation, AnilistScore, MediaCoverImage, AnilistMediaCharacter, AnilistMedia, AnilistTitle, \
    AnilistMediaInfo, MediaFormat, MediaSource, MediaSeason, MediaStatus, MediaRelation, CharacterRole, AnilistCharacter, AnilistTag, AnilistStudio,\
    AnilistMediaBase, MediaType, MediaGenre
from AnillistPython.models.media import AnilistMediaTrailer, AnilistEpisode


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
        return AnilistTitle()
    return AnilistTitle(**title_data)

def parse_cover_image(img_data: Optional[dict]) -> Optional['MediaCoverImage']:
    if not img_data:
        return MediaCoverImage()
    return MediaCoverImage(
        extraLarge=img_data.get("extraLarge"),
        large=img_data.get("large"),
        medium=img_data.get("medium"),
        color=img_data.get("color")
    )


def parse_score(score_data: Optional[dict], media_id: int) -> Optional[AnilistScore]:
    if not score_data:
        return AnilistScore(id = media_id)

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
        return AnilistMediaInfo(id = media_id)

    return AnilistMediaInfo(
        id=media_id,
        format=MediaFormat.from_str(info_data.get("format")),
        source=MediaSource.from_str(info_data.get("source")),
        country_origin=info_data.get("countryOfOrigin"),
        season=MediaSeason.from_str(info_data.get("season")),
        status=MediaStatus.from_str(info_data.get("status")),
    )

def parse_genres(genres: List[str])-> List[MediaGenre]:
    if not genres:
        return []
    genre_list = []
    for genre in genres:
        genre_list.append(MediaGenre.from_str(genre))
    return genre_list


def parse_tag(tag_data: Optional[dict], media_id: int) -> Optional[AnilistTag]:
    if not tag_data:
        return None
    return AnilistTag(
        id=tag_data.get("id"),
        name=tag_data.get("name"),
        description=tag_data.get("description"),
        category=tag_data.get("category"),
        isAdult=tag_data.get("isAdult")
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

def parse_episode(streaming_data: Optional[dict], media_id: int) -> Optional[AnilistEpisode]:
    if not streaming_data:
        return None
    return AnilistEpisode(
        media_id=media_id,
        title=streaming_data.get('title'),
        thumbnail=streaming_data.get('thumbnail'),
        official_url=streaming_data.get('url'),
        official_site=streaming_data.get('site'),
    )

def parse_media_base(
    media_data: Dict[str, Any],
    media_type: MediaType = None,
    fields: Optional[Set[str]] = None
) -> Optional[AnilistMediaBase]:
    media_id = media_data.get("id")
    if not media_id:
        return None


    # Helper to check if a field should be included
    include_field = lambda field: fields is None or field in fields

    # Parse fields conditionally based on 'fields' set
    title = parse_title(media_data.get("title")) if include_field("title") else None
    start_date = parse_date(media_data.get("startDate")) if include_field("startDate") else None
    end_date = parse_date(media_data.get("endDate")) if include_field("endDate") else None
    image = parse_cover_image(media_data.get("coverImage")) if include_field("coverImage") else None
    info = parse_media_info(media_data, media_id) if include_field("info") else None
    score = parse_score(media_data, media_id) if include_field("score") else None

    character_list = []
    if (fields is None or "characters" in fields) and (characters := media_data.get("characters")):
        for character in characters.get("edges", []):
            if (character_data := parse_character(character, media_id)):
                character_list.append(character_data)

    tag_list = []
    if (fields is None or "tags" in fields) and (tags := media_data.get("tags")):
        for tag in tags:
            if (tag_data := parse_tag(tag, media_id)):
                tag_list.append(tag_data)

    studio_list = []
    if (fields is None or "studios" in fields) and (studios := media_data.get("studios")):
        for studio in studios.get("edges", []):
            if (studio_data := parse_studio(studio, media_id)):
                studio_list.append(studio_data)

    return AnilistMediaBase(
        id=media_id,
        idMal=media_data.get("idMal"),
        media_type=media_type or MediaType.from_str(media_data.get("type")),
        title=title,
        coverImage=image,
        bannerImage=media_data.get("bannerImage"),
        description=media_data.get("description"),
        genres=parse_genres(media_data.get("genres")),
        score=score,
        info=info,
        synonyms=media_data.get("synonyms"),
        tags=tag_list,
        startDate=start_date,
        endDate=end_date,
        studios=studio_list,
        characters=character_list,
        trailer=parse_trailer(media_data.get("trailer")) if fields is None or "trailer" in fields else None,
        siteUrl=media_data.get("siteUrl"),
        isAdult=media_data.get("isAdult"),
        duration=media_data.get("duration"),
        episodes=media_data.get("episodes"),
        chapters=media_data.get("chapters"),
        volumes=media_data.get("volumes"),
    )

def parse_relation(relation_data: Optional[dict], media_id: int, fields: Optional[Set[str]] = None) -> Optional['AnilistRelation']:
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
        media=parse_media_base(node, fields=fields)
    )

def parse_recommendation(media_id: int, media_data: Dict[str, Any], fields: Optional[Set[str]] = None) -> Optional[AnilistRecommendation]:
    """
    :param media_id: id of media
    :param media_data: value at data[AnilistMedia][recommendations][nodes][mediaRecommendation]
    :return: data class of AnilistRecommendation
    """
    if not media_data:
        return None

    return AnilistRecommendation(
        from_media_id=media_id,
        media=parse_media_base(media_data, fields=fields)
    )

def parse_media(
    media_data: dict,
    media_type: MediaType,
    media_fields: Optional[Set[str]] = None,
    relation_fields: Optional[Set[str]] = None,
    recommendation_fields: Optional[Set[str]] = None
) -> Optional[AnilistMedia]:
    media_id = media_data.get("id")
    if not media_id:
        return None

    media = parse_media_base(media_data, media_type, media_fields)

    relation_list = []
    if (media_fields is None or "relations" in media_fields) and relation_fields is not None:
        relations = media_data.get("relations")
        if relations:
            for relation in relations.get("edges", []):
                rel_data = parse_relation(relation, media_id, relation_fields)
                if rel_data:
                    relation_list.append(rel_data)

    recommendation_list = []
    if (media_fields is None or "recommendations" in media_fields) and recommendation_fields is not None:
        recommendations = media_data.get("recommendations")
        if recommendations:
            for recommendation in recommendations.get("nodes", []):
                media_rec = recommendation.get("mediaRecommendation")
                if media_rec:
                    recom_data = parse_recommendation(media_id, media_rec, recommendation_fields)
                    if recom_data:
                        recommendation_list.append(recom_data)

    return AnilistMedia(
        **vars(media),
        relations=relation_list,
        recommendations=recommendation_list
    )

def parse_graphql_media_data(graphql_media_data: Dict[str, Any], media_type: MediaType) -> Optional[AnilistMedia]:
    media_data = graphql_media_data.get("data", {}).get("AnilistMedia")
    if not media_data:
        print("'AnilistMedia' not found trying to fetch 'media'")
        media_data = graphql_media_data.get("data", {}).get("media")
    if not media_data:
        print("media data is empty")
        return None

    return parse_media(media_data, media_type)

if __name__ == '__main__':
    from timeit import timeit
    from pprint import pprint
    from pathlib import Path
    import json
    path = Path(r"D:\Program\AnilistPython\AnillistPython\samples\media_2.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    media_data = data["data"]["media"]

    # Define field sets
    minimal_fields = {"id", "title", "coverImage", "score", "siteUrl"}
    full_fields = None  # This means "parse everything"

    # Wrap parse_media in a callable for benchmarking
    def run_minimal():
        parse_media(media_data, MediaType.ANIME, media_fields=minimal_fields)

    def run_full():
        parse_media(media_data, MediaType.ANIME, media_fields=full_fields)

    # Benchmark both
    runs = 10
    min_time = timeit(run_minimal, number=runs)
    full_time = timeit(run_full, number=runs)

    print(f"✅ Benchmark Results ({runs} runs):")
    print(f"Minimal fields parse time:     {min_time:.4f} seconds")
    print(f"Full parse time:               {full_time:.4f} seconds")
    print(f"Speedup:                       {full_time / min_time:.2f}x faster using minimal fields")

    # Optional: print one actual result
    print("\nParsed media (minimal):")
    media = parse_media(media_data, MediaType.ANIME, media_fields=minimal_fields)
    # pprint(media)