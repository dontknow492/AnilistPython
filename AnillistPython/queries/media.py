import hashlib
from typing import Optional, List, Union, overload, override, Tuple, Set

page_query: str = """
    Page (page: $page, perPage: $perpage) {
                        pageInfo {
                            total
                            currentPage
                            lastPage
                            hasNextPage
                        }
                    """


class MediaQueryBuilderBase:
    def __init__(self):
        self.fields = ["id", "idMal", "type"]
        self._included_fields = {"id", "idMal", "type"}

    def include_title(self):
        self._included_fields.add('title')
        self.fields.append("""
            title {
                romaji
                english
                native
            }""")
        return self

    def include_description(self):
        self._included_fields.add('description')
        self.fields.append("""
            description""")
        return self

    def include_images(self,
                       include_large: bool = True,
                       include_medium: bool = False,
                       include_extra_large: bool = False,
                       include_color: bool = False,
                       ):
        self._included_fields.add('coverImage')
        cover_fields = []
        if include_large:
            cover_fields.append("large")
        if include_medium:
            cover_fields.append("medium")
        if include_extra_large:
            cover_fields.append("extraLarge")
        if include_color:
            cover_fields.append("color")

        field = " ".join(cover_fields)

        if cover_fields:
            cover_block = f"""
            coverImage {{ {field} }}"""
            self.fields.append(cover_block)
        return self

    def include_banner_image(self):
        self._included_fields.add('bannerImage')
        self.fields.append("""
            bannerImage""")
        return self

    def include_synonyms(self):
        self.fields.append("""
            synonyms""")
        return self

    def include_tags(self, include_id=True, include_name=True, include_description=False,
                     include_category=False, include_is_adult=False):
        self._included_fields.add('tags')
        fields = []
        if include_id:
            fields.append("id")
        if include_name:
            fields.append("name")
        if include_description:
            fields.append("description")
        if include_category:
            fields.append("category")
        if include_is_adult:
            fields.append("isAdult")

        self.fields.append(
            f"""
            tags {{
                {' '.join(fields)}
            }}"""
        )
        return self

    def include_genres(self):
        self._included_fields.add('genres')
        self.fields.append("""
            genres""")
        return self

    def include_studios(self, is_main: bool = True):
        self._included_fields.add('studios')
        self.fields.append(
            f"""
            studios(isMain: {"true" if is_main else "false"}) {{
                edges {{
                    node {{
                        id
                        name
                    }}
                }}
            }}
            """
        )
        return self

    def include_score(self):
        self._included_fields.add('score')
        self.fields.append(
            """
            averageScore
            meanScore
            popularity
            favourites"""
        )
        return self

    def include_info(self):
        self._included_fields.add('info')
        self.fields.append(
            """
            format
            source
            countryOfOrigin
            season
            status"""
        )
        return self

    def include_dates(self):
        self._included_fields.add('startDate')
        self._included_fields.add('endDate')
        self.fields.append(
            """
            startDate { year month day }
            endDate { year month day }"""
        )
        return self


    def include_characters(self, page: int = 1, perpage: int = 10, include_description=False, include_age=False,
                           include_dob=False):
        self._included_fields.add('characters')
        node_fields = [
            "id",
            "name { full }",
            "image { large }"
        ]

        if include_age:
            node_fields.append("age")
        if include_dob:
            node_fields.append("dateOfBirth { year month day }")
        if include_description:
            node_fields.append("description")

        character_fragment = f"""
            characters(page: {page}, perPage: {perpage}) {{
                edges {{

                    role
                    node {{
                        {' '.join(node_fields)}
                    }}
                }}
            }}"""

        self.fields.append(character_fragment)
        return self

    def include_trailer(self):
        self._included_fields.add('trailer')
        self.fields.append("""
            trailer {{
                id
                site
                thumbnail
            }}""")
        return self

    def include_is_adult(self):
        self._included_fields.add("isAdult")
        self.fields.append("""
            isAdult""")
        return self

    def include_anilist_site(self):
        self._included_fields.add('siteUrl')
        self.fields.append("""
            siteUrl""")
        return self

    def include_myanimelist_id(self):
        self._included_fields.add('idMal')
        self.fields.append("""
            idMal""")
        return self

    def include_anime_fields(self):
        self._included_fields.add('episodes')
        self._included_fields.add('duration')
        self.fields.append("""
            episodes
            duration""")
        return self

    def include_manga_fields(self):
        self._included_fields.add('chapters')
        self._included_fields.add('genres')
        self.fields.append("""
            chapters
            volumes""")
        return self

    def field(self) -> List[str]:
        return self.fields

    def included_options(self)->Set:
        return self._included_fields

    def build(self) -> str:
        fields_str = ' '.join(self.fields)
        return f"""query ($id: Int) {{
        Media(id: $id) {{
            {fields_str}
          }}
    }}""".strip()

    def include_all(self, is_anime: bool = False, page:int = 1, perpage: int = 5):
        self.include_myanimelist_id()
        self.include_title()
        self.include_description()
        self.include_images(True, True, True, True)
        self.include_banner_image()
        self.include_genres()
        self.include_score()
        self.include_info()
        self.include_synonyms()
        self.include_tags(True, True, True, True, True)
        self.include_dates()
        self.include_studios()
        self.include_characters(page, perpage, True, True, True)
        self.include_trailer()
        self.include_anilist_site()
        self.include_is_adult()
        self.include_anime_fields() if is_anime else self.include_manga_fields()

        return self

    def build_full(self, is_anime: bool, page:int = 1, perpage: int = 5) -> str:
        # Call all include methods you want in the full query
        self.include_all(is_anime, page, perpage)
        # You can add more includes if you define them later

        return self.build()

    def reset_build(self):
        self.fields = ["id", "idMal", "type"]
        self._included_fields = {"id", "idMal", "type"}

    def __hash__(self):
        return int(self.stable_hash(), 16)

    def stable_hash(self) -> str:
        # Ensure every item is a string (and flatten if needed)
        fields = self.included_options()
        normalized = []
        for item in fields:
            if isinstance(item, set):
                # Flatten nested sets (e.g. {'id', 'idMal'})
                normalized.extend(str(subitem) for subitem in sorted(item))
            else:
                normalized.append(str(item))

        combined = '|'.join(sorted(normalized))
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()

    def __eq__(self, other):
        if not isinstance(other, MediaQueryBuilderBase):
            return NotImplemented
        return sorted(self.fields) == sorted(other.fields)

class MediaQueryBuilder(MediaQueryBuilderBase):
    def __init__(self):
        super().__init__()
        self._included_relations_fields = set()
        self._included_recommendations_fields = set()

    def include_relations(self, query: MediaQueryBuilderBase):
        self._included_relations_fields = query.included_options()
        self._included_fields.add('relations')
        relation_field = query.field()
        relation_query = " ".join(relation_field)
        self.fields.append(
            f"""
            relations{{
                edges {{
                    relationType
                    node {{
                        {relation_query}
                    }}
                }}
            }}"""
        )
        return self

    def include_recommendations(self, query: MediaQueryBuilderBase, page: int = 1, perpage: int = 10):
        self._included_fields.add('recommendations')
        self._included_recommendations_fields = query.included_options()
        recommendation_field = query.field()
        recommendation_str = " ".join(recommendation_field)
        self.fields.append(
            f"""
            recommendations(page: {page}, perPage: {perpage}) {{
                pageInfo {{
                    currentPage
                    hasNextPage
                }}
                nodes {{
                    mediaRecommendation {{
                        {recommendation_str}
                    }}
                }}
            }}"""
        )
        return self

    @override
    def include_all(self, is_anime: bool, page:int, perpage: int,
                    relations_build: MediaQueryBuilderBase, recomendation_build: MediaQueryBuilderBase):
        super().include_all(is_anime, page, perpage)
        self.include_recommendations(recomendation_build, page=page, perpage=perpage)
        self.include_relations(relations_build)
        return self


    @override
    def build_full(self, is_anime: bool, page: int, perpage: int,
                relations_build: MediaQueryBuilderBase, recomendation_build: MediaQueryBuilderBase) -> str:
        # Call all include methods you want in the full query
        self.include_all(is_anime, page, perpage, relations_build, recomendation_build)
        # You can add more includes if you define them later

        return self.build()

    def included_options(self)->Tuple[Set, Set, Set]:
        return self._included_fields, self._included_relations_fields, self._included_recommendations_fields

if __name__ == "__main__":
    from pprint import pprint
    relation_builder = MediaQueryBuilderBase().include_all()
    recommendation_builder = MediaQueryBuilderBase().include_all()
    query = MediaQueryBuilder().include_all(False, 1, 10, relation_builder, recommendation_builder)
    print(relation_builder.included_options())

    print(query.fields)
    pprint(query.stable_hash())#1028056373099110810
