from typing import Union, List, Set, Optional

from AnillistPython.queries.media import MediaQueryBuilder
from AnillistPython.models import MediaSeason, MediaSource, MediaStatus, MediaType, MediaFormat, MediaRelation, MediaSort


class SearchQueryBuilder:
    def __init__(self):
        self.variables = {}
        self.filters = []

        self._included_options: Set[str] = set()

    def set_search(self, query: str):
        # self.filters.append("search: $query")
        self.variables["query"] = query
        return self

    def set_sort(self, sort: MediaSort):
        if "sort" in self._included_options:
            raise ValueError('There can be only one argument named "sort" ')
        self.filters.append(f'sort: {sort.value}')
        return self

    def set_type(self, media_type: MediaType):  # ANIME or MANGA
        self.filters.append(f'type: {media_type.value}')
        return self

    def set_formats(self, media_formats: List[MediaFormat], is_excluded: bool = False):
        values = ", ".join(media_format.value for media_format in media_formats)
        if is_excluded:
            self.filters.append(f'format_not_in: [{values}]')
        else:
            self.filters.append(f'format_in: [{values}]')
        return self

    def set_status(self, status: List[MediaStatus], is_excluded: bool = False):
        values = ", ".join(media_format.value for media_format in status)
        if is_excluded:
            self.filters.append(f'status_not_in: [{values}]')
        else:
            self.filters.append(f'status_in: [{values}]')
        return self

    def set_sources(self, sources: list[MediaSource]):
        values = ", ".join(source.value for source in sources)
        self.filters.append(f'source_in: [{values}]')
        return self

    def set_season(self, season: MediaSeason, year: Optional[int] = None):
        self.filters.append(f'season: {season.value}')
        if year is not None:
            self.filters.append(f'seasonYear: {year}')
        return self

    def set_genres(self, include: list[str] = None, exclude: list[str] = None):
        if include:
            genre_list = ', '.join(f'"{g}"' for g in include)
            self.filters.append(f'genre_in: [{genre_list}]')
        if exclude:
            genre_list = ', '.join(f'"{g}"' for g in exclude)
            self.filters.append(f'genre_not_in: [{genre_list}]')
        return self

    def set_tags(self, include: list[str] = None, exclude: list[str] = None):
        if include:
            tag_list = ', '.join(f'"{t}"' for t in include)
            self.filters.append(f'tag_in: [{tag_list}]')
        if exclude:
            tag_list = ', '.join(f'"{t}"' for t in exclude)
            self.filters.append(f'tag_not_in: [{tag_list}]')
        # self.filters.append(f'minimumTagRank: {minimum_tags_rank}')
        return self

    def set_score_range(self, min_score: int = None, max_score: int = None):
        if min_score is not None:
            self.filters.append(f'averageScore_greater: {min_score}')
        if max_score is not None:
            self.filters.append(f'averageScore_lesser: {max_score}')
        return self

    def set_episodes_range(self, min_episodes: int = None, max_episodes: int = None):
        if min_episodes is not None:
            self.filters.append(f'episodes_greater: {min_episodes}')  # or episodes_gt
        if max_episodes is not None:
            self.filters.append(f'episodes_lesser: {max_episodes}')  # or episodes_lt
        return self

    def set_duration_range(self, min_duration: int = None, max_duration: int = None):
        """Duration in minutes"""
        if min_duration is not None:
            self.filters.append(f'duration_greater: {min_duration}')
        if max_duration is not None:
            self.filters.append(f'duration_lesser: {max_duration}')
        return self

    def set_chapters_range(self, min_chapters: int = None, max_chapters: int = None):
        if min_chapters is not None:
            self.filters.append(f'chapters_greater: {min_chapters}')
        if max_chapters is not None:
            self.filters.append(f'chapters_lesser: {max_chapters}')
        return self

    def set_year_range(self, min_year: int = None, max_year: int = None):
        if min_year is not None:
            start_date = int(f"{min_year}0101")
            self.filters.append(f"startDate_greater: {start_date}")
        if max_year is not None:
            end_date = int(f"{max_year}1231")
            self.filters.append(f"startDate_lesser: {end_date}")
        return self

    def set_adult(self, is_adult: bool = False):
        self.filters.append(f'isAdult: {"true" if is_adult else "false"}')
        return self

    def set_page(self, page: int = 1, per_page: int = 10):
        self.variables["page"] = page
        self.variables["perpage"] = per_page
        return self

    def build(self, media_fields: MediaQueryBuilder) -> str:
        if isinstance(media_fields, MediaQueryBuilder):
            media_fields = media_fields.field() # return List[str]
            media_fields_str = ' '.join(media_fields)

        # elif isinstance(media_fields, str):
        #     media_fields_str = media_fields

        else:
            raise TypeError('media_fields must be either str or list or MediaQueryBuilder')

        filter_str = ', '.join(self.filters)
        return f"""
                query ($query: String, $page: Int, $perpage: Int) {{
                    Page(page: $page, perPage: $perpage) {{
                        pageInfo {{
                            total
                            currentPage
                            lastPage
                            hasNextPage
                        }}
                        media(search: $query, {filter_str}) {{  
                            {media_fields_str}
                        }}
                    }}
                }}
                """.strip() #



    def reset_build(self):
        self.filters = []
        self.variables = {}

if __name__ == "__main__":
    media_query = MediaQueryBuilder()
    builder = SearchQueryBuilder().set_sort(MediaSort.TRENDING_DESC).set_search("one")
    query = builder.build(media_query)
    print(query)
