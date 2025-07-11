import asyncio
import json
# from calendar import error
from pathlib import Path
from pprint import pprint
from typing import Optional, Union, List, Dict, Any

import httpx
from gql import Client, gql
from gql.transport.exceptions import TransportError, TransportServerError, TransportQueryError
from gql.transport.httpx import HTTPXTransport, HTTPXAsyncTransport

from loguru import logger
from graphql import ExecutionResult, GraphQLError

from AnillistPython.models import MediaFormat, MediaSource, AnilistSearchResult
from AnillistPython.models import AnilistRecommendation, AnilistRelation, AnilistMedia, MediaType, MediaSort, MediaStatus
from AnillistPython.queries import MediaQueryBuilder, SearchQueryBuilder, UserActivityQueryBuilder, MediaQueryBuilderBase
from AnillistPython.parser import parse_recommendation, parse_graphql_media_data, parse_searched_media, \
    parse_relation, parse_media

import copy

class AniListClient:
    def __init__(self, url="https://graphql.anilist.co"):
        try:
            self.transport = HTTPXAsyncTransport(url=url)
            self.client = Client(transport=self.transport, fetch_schema_from_transport=True)
        except httpx.ConnectError as e:
            logger.error(f"Failed to connect to AniList API: {e}")
            raise ConnectionError("Unable to connect to AniList API.") from e
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during schema fetch: {e.response.status_code} {e.response.text}")
            raise
        except TransportServerError as e:
            logger.error(f"Transport server error: {e}")
            raise
        except TransportQueryError as e:
            logger.error(f"GraphQL query error: {e}")
            raise
        except Exception as e:
            logger.exception("Unexpected error during client initialization")
            raise

        self.session = None

        self.media_query_builder = MediaQueryBuilder()
        self.search_query_builder = SearchQueryBuilder()
        self.user_activity_query_builder = UserActivityQueryBuilder()

    async def connect(self):
        try:
            self.session = await self.client.connect_async()
        except (httpx.ConnectError, httpx.ConnectTimeout) as e:
            logger.error("Failed to connect to AniList API: %s", e)
            raise ConnectionError("Unable to connect to AniList API.") from e
        except Exception as e:
            logger.error("Unexpected error during connection: %s", e)
            raise

    async def close(self):
        await self.client.close_async()

    async def fetch(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self.session:
            await self.connect()

        try:
            result = await self.session.execute(gql(query), variable_values=variables)

            # print(result)

            if not result or not isinstance(result, dict):
                logger.warning("Received empty or malformed response: %s", result)
                raise ValueError("Received empty or malformed response from AniList API.")

            return result

        except httpx.HTTPStatusError as e:
            logger.error("HTTP error: %s (status: %s)", e.response.text, e.response.status_code)
            raise
        except httpx.RequestError as e:
            logger.error("Request error while contacting AniList API: %s", e)
            raise
        except TransportError as e:
            logger.error("Transport error: %s", e)
            raise
        except GraphQLError as e:
            logger.error("GraphQL execution error: %s", e.message)
            raise
        except Exception as e:
            logger.exception("Unhandled exception during fetch")
            raise

    async def get_anime(self, media_id: int, builder: Optional[MediaQueryBuilder]) -> Optional[AnilistMedia]:
        if not builder:
            builder = self.media_query_builder
        builder = copy.deepcopy(builder)
        builder.include_anime_fields()
        query = builder.build()
        logger.debug(f"query: \n{query}, media_id: {media_id}")
        result = await self.fetch(query, variables={"id": media_id})
        logger.debug(f"result: {result}, media_id: {media_id}")
        anime = parse_graphql_media_data(result, MediaType.ANIME)
        return anime


    async def search_anime(self, builder: Optional[MediaQueryBuilder], filters: SearchQueryBuilder,
                        query: Optional[str], page: int = 1, perpage: int = 5) -> AnilistSearchResult:
        if not builder:
            builder = self.media_query_builder
        builder = copy.deepcopy(builder)
        filters = copy.deepcopy(filters)
        builder.include_anime_fields()
        if query:
            variables = {"page": page, "perpage": perpage, "query": query}
        else:
            variables = {"page": page, "perpage": perpage}
        filters.set_type(MediaType.ANIME)

        search_query = filters.build(builder)
        # logger.debug(f"query: \n{search_query}")
        result = await self.fetch(search_query, variables)

        # with open("animes.json", "w", encoding="utf-8") as f:
        #     json.dump(result, f, ensure_ascii=False, indent=4)
        #
        # with open("animes.json", "r", encoding="utf-8") as f:
        #     animes = json.load(f)

        fields = builder.included_options()
        return parse_searched_media(result, MediaType.ANIME, fields[0], fields[1], fields[2])


    async def get_manga(self, media_id: int, builder: Optional[MediaQueryBuilder]) -> AnilistMedia:
        if not builder:
            builder = self.media_query_builder
        builder = copy.deepcopy(builder)
        builder.include_manga_fields()
        query = builder.build()
        result = await self.fetch(query)
        manga = parse_graphql_media_data(result, MediaType.MANGA)
        return manga

    async def search_manga(self, builder: Optional[MediaQueryBuilder], filters: SearchQueryBuilder,
                        query: Optional[str], page: int = 1, perpage: int = 5) -> AnilistSearchResult:
        if not builder:
            builder = self.media_query_builder
        builder = copy.deepcopy(builder)
        filters = copy.deepcopy(filters)
        builder.include_manga_fields()
        if query:
            variables = {"page": page, "perpage": perpage, "query": query}
        else:
            variables = {"page": page, "perpage": perpage}
        filters.set_type(MediaType.MANGA)
        search_query = filters.build(builder)
        result = await self.fetch(search_query, variables)
        return parse_searched_media(result, MediaType.MANGA)

    async def get_recommendations(self, builder: MediaQueryBuilderBase, media_id: int, page: int = 1, perpage: int = 5) -> Optional[List[AnilistRecommendation]]:
        if not builder:
            raise ValueError("Builder cannot be None")
        fields = builder.field()
        fields_str = " ".join(fields)
        query =  f"""
        query ($id: Int, $page: Int, $perPage: Int) {{
        Media(id: $id) {{
            recommendations(page: $page, perPage: $perPage) {{
                pageInfo {{
                    total
                    currentPage
                    lastPage
                    hasNextPage
                    perPage
                }}
                nodes {{
                    mediaRecommendation {{
                        {fields_str}
                    }}
                }}
            }}
        }}
    }}""".strip()
        result = await self.fetch(query, {"id": media_id, "page": page, "perpage": perpage})
        recommendations = result.get("data", {}).get("AnilistMedia",{}).get("recommendations", {}).get("nodes", [])
        return [parse_recommendation(media_id, recommendation.get("mediaRecommendations")) for recommendation in recommendations]


    async def get_relations(self, builder: MediaQueryBuilderBase, media_id: int) -> Optional[List[AnilistRelation]]:
        if not builder:
            raise ValueError("Builder cannot be None")
        fields = builder.field()
        fields_str = " ".join(fields)
        query = f"""
        query ($id: Int) {{
            AnilistMedia(id: $id) {{
                relations{{
                    edges {{
                        relationType
                        node {{
                            {fields_str}
                        }}
                    }}
                }}
            }}
        }}""".strip()
        result = await self.fetch(query, {"id": media_id})
        relations = result.get("data", {}).get("AnilistMedia", {}).get("relations", {}).get("edges", [])
        return [parse_relation(relation, media_id) for relation in relations]

    async def get_trending(self, fields: MediaQueryBuilder, media_type: MediaType, page: int = 1, per_page: int = 5)->AnilistSearchResult:
        search_query = SearchQueryBuilder().set_sort(MediaSort.TRENDING_DESC)
        if media_type == MediaType.ANIME:
            return await self.search_anime(fields, search_query, None, page, per_page)
        else:
            return await self.search_manga(fields, search_query, None, page, per_page)

    async def get_top_popular(self, fields: MediaQueryBuilder, media_type: MediaType, page: int = 1, per_page: int = 5)->AnilistSearchResult:
        search_query = SearchQueryBuilder().set_sort(MediaSort.POPULARITY_DESC)
        if media_type == MediaType.ANIME:
            return await self.search_anime(fields, search_query, None, page, per_page)
        else:
            return await self.search_manga(fields, search_query, None, page, per_page)

    async def get_top_rated(self, fields: MediaQueryBuilder, media_type: MediaType, page: int = 1, per_page: int = 5)->AnilistSearchResult:
        search_query = SearchQueryBuilder().set_sort(MediaSort.SCORE_DESC)
        if media_type == MediaType.ANIME:
            search_query.set_episodes_range(5)
            search_query.set_score_range(80, 99)
            return await self.search_anime(fields, search_query, None, page, per_page)
        else:
            search_query.set_chapters_range(5)
            search_query.set_score_range(80, 99)
            return await self.search_manga(fields, search_query, None, page, per_page)

    async def get_latest(self, fields: MediaQueryBuilder, media_type: MediaType, page: int = 1, per_page: int = 5)->AnilistSearchResult:
        search_query = SearchQueryBuilder().set_sort(MediaSort.START_DATE_DESC).set_status([MediaStatus.RELEASING,])
        # print("search_query:", search_query.build(fields))
        if media_type == MediaType.ANIME:
            search_query.set_formats([MediaFormat.TV,])
            search_query.set_sources([MediaSource.MANGA, MediaSource.LIGHT_NOVEL, MediaSource.WEB_NOVEL])
            return await self.search_anime(fields, search_query, None, page, per_page)
        else:
            return await self.search_manga(fields, search_query, None, page, per_page)

    async def get_user_activity(self, query: str, variables: dict = None) -> dict:
        raise NotImplementedError("Not implemented")
        # pass


    async def get_episode(self, media_id: int):
        query = """
        query ($id: Int) {
          Media(id: $id) {
            episodes
            streamingEpisodes {
              title
              thumbnail
              url
              site
            }
            
          }
        }"""
        variables = {"id": media_id}
        result = await self.fetch(query, variables)

if __name__ == '__main__':
    print("ets")
    async def main():
        relation_builder = MediaQueryBuilderBase()
        recommendation_builder = MediaQueryBuilderBase()
        media_query_builder = MediaQueryBuilder().include_score()
        search_query_builder = SearchQueryBuilder()
        anilist = AniListClient()
        await anilist.connect()

        anime = await anilist.get_anime(1, media_query_builder)
        print(anime)

    asyncio.run(main())
