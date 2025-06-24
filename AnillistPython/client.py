import asyncio
# from calendar import error
from pathlib import Path
from typing import Optional, Union, List, Dict, Any
from gql import Client, gql
from gql.transport.exceptions import TransportError
from gql.transport.httpx import HTTPXTransport

from loguru import logger
from graphql import ExecutionResult, GraphQLError

from models import AnilistRecommendation, AnilistRelation, AnilistMedia, MediaType
from queries import MediaQueryBuilder, SearchQueryBuilder, UserActivityQueryBuilder, MediaQueryBuilderBase
from parser import parse_recommendation, parse_graphql_media_data, parse_searched_media, \
    parse_relation, parse_media



class AniListClient:
    def __init__(self, url="https://graphql.anilist.co"):
        self.transport = HTTPXTransport(url=url)
        path = Path("schema.graphql")
        with open(path, "r", encoding="utf-16") as f:
            schema = f.read()
        self.client = Client(transport=self.transport, schema=schema)

        self.media_query_builder = MediaQueryBuilder()
        self.search_query_builder = SearchQueryBuilder()
        self.user_activity_query_builder = UserActivityQueryBuilder()

    async def fetch(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        async with self.client as session:
            try:
                result = await session.execute(gql(query), variable_values=variables)
            # errors = ExecutionResult().errors
                return result
            except TransportError as e:
                logger.error(e)
            except GraphQLError as e:
                logger.error(e)

    async def get_anime(self, media_id: int, builder: Optional[MediaQueryBuilder]) -> Optional[AnilistMedia]:
        if not builder:
            builder = self.media_query_builder
        builder.include_anime_fields()
        query = builder.build()
        logger.debug(f"query: \n{query}, media_id: {media_id}")
        result = await self.fetch(query, variables={"id": media_id})
        anime = parse_graphql_media_data(result)
        return anime


    async def search_anime(self, builder: Optional[MediaQueryBuilder], filters: SearchQueryBuilder,
                        query: str, page: int = 1, perpage: int = 5) -> List[AnilistMedia]:
        if not builder:
            builder = self.media_query_builder
        builder.include_anime_fields()
        variables = {"page": page, "perpage": perpage, "query": query}
        filters.set_type(MediaType.ANIME)
        search_query = filters.build(builder)
        logger.debug(f"query: \n{search_query}")
        result = await self.fetch(search_query, variables)
        return parse_searched_media(result)


    async def get_manga(self, media_id: int, builder: Optional[MediaQueryBuilder]) -> AnilistMedia:
        if not builder:
            builder = self.media_query_builder
        builder.include_manga_fields()
        query = builder.build()
        result = await self.fetch(query)
        manga = parse_graphql_media_data(result)
        return manga

    async def search_manga(self, builder: Optional[MediaQueryBuilder], filters: SearchQueryBuilder,
                        query: str, page: int = 1, perpage: int = 5) -> List[AnilistMedia]:
        if not builder:
            builder = self.media_query_builder
        builder.include_manga_fields()
        variables = {"page": page, "perpage": perpage, "query": query}
        filters.set_type(MediaType.MANGA)
        search_query = filters.build(builder)
        result = await self.fetch(search_query, variables)
        return parse_searched_media(result)

    async def get_recommendations(self, builder: MediaQueryBuilderBase, media_id: int, page: int = 1, perpage: int = 5) -> Optional[List[AnilistRecommendation]]:
        if not builder:
            raise ValueError("Builder cannot be None")
        fields = builder.field()
        fields_str = " ".join(fields)
        query =  f"""
        query ($id: Int) {{
            AnilistMedia(id: $id) {{
                recommendations {{
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


    async def get_user_activity(self, query: str, variables: dict = None) -> dict:
        pass


if __name__ == '__main__':
    async def main():
        relation_builder = MediaQueryBuilderBase()
        recommendation_builder = MediaQueryBuilderBase()
        media_query_builder = MediaQueryBuilder().include_all(True, 1, 1, relation_builder, recommendation_builder)
        search_query_builder = SearchQueryBuilder()
        anilist = AniListClient()
        # await anilist.search_anime(media_query_builder, search_query_builder, "one")
        # await anilist.get_anime(1, media_query_builder)

    asyncio.run(main())
