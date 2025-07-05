import hashlib
import json
from typing import Union, List, Set, Optional

from AnillistPython.queries.media import MediaQueryBuilder
from AnillistPython.models import (MediaSeason, MediaSource, MediaStatus, MediaType, MediaFormat, MediaRelation,
                                MediaSort, MediaGenre)


class SearchQueryBuilder:
    def __init__(self):
        self.variables = {}
        self.filters = []
        self._included_options: Set[str] = set()

    def _add_or_replace_filter(self, key: str, value: str):
        pattern = f"{key}:"
        existing = next((i for i, f in enumerate(self.filters) if f.startswith(pattern)), None)
        filter_str = f"{key}: {value}"
        if existing is not None:
            self.filters[existing] = filter_str
        else:
            self.filters.append(filter_str)

    def set_search(self, query: str):
        self.variables["query"] = query
        return self

    def set_sort(self, sort: MediaSort):
        if "sort" in self._included_options:
            raise ValueError('There can be only one argument named "sort"')
        self._included_options.add("sort")
        self._add_or_replace_filter("sort", sort.value)
        return self

    def set_type(self, media_type: MediaType):
        self._add_or_replace_filter("type", media_type.value)
        return self

    def set_formats(self, media_formats: List[MediaFormat], is_excluded: bool = False):
        values = ", ".join(fmt.value for fmt in media_formats)
        key = "format_not_in" if is_excluded else "format_in"
        self._add_or_replace_filter(key, f"[{values}]")
        return self

    def set_status(self, status: List[MediaStatus], is_excluded: bool = False):
        values = ", ".join(s.value for s in status)
        key = "status_not_in" if is_excluded else "status_in"
        self._add_or_replace_filter(key, f"[{values}]")
        return self

    def set_sources(self, sources: List[MediaSource]):
        values = ", ".join(s.value for s in sources)
        self._add_or_replace_filter("source_in", f"[{values}]")
        return self

    def set_season(self, season: MediaSeason, year: Optional[int] = None):
        self._add_or_replace_filter("season", season.value)
        if year is not None:
            self._add_or_replace_filter("seasonYear", str(year))
        return self

    def set_genres(self, include: List[Union[MediaGenre, str]] = None, exclude: List[Union[MediaGenre, str]] = None):
        if include:
            values = ", ".join(f'"{g.value if isinstance(g, MediaGenre) else g}"' for g in include)
            self._add_or_replace_filter("genre_in", f"[{values}]")
        if exclude:
            values = ", ".join(f'"{g.value if isinstance(g, MediaGenre) else g}"' for g in exclude)
            self._add_or_replace_filter("genre_not_in", f"[{values}]")
        return self

    def set_tags(self, include: List[str] = None, exclude: List[str] = None):
        if include:
            values = ", ".join(f'"{t}"' for t in include)
            self._add_or_replace_filter("tag_in", f"[{values}]")
        if exclude:
            values = ", ".join(f'"{t}"' for t in exclude)
            self._add_or_replace_filter("tag_not_in", f"[{values}]")
        return self

    def set_score_range(self, min_score: int = None, max_score: int = None):
        if min_score is not None:
            self._add_or_replace_filter("averageScore_greater", str(min_score))
        if max_score is not None:
            self._add_or_replace_filter("averageScore_lesser", str(max_score))
        return self

    def set_episodes_range(self, min_episodes: int = None, max_episodes: int = None):
        if min_episodes is not None:
            self._add_or_replace_filter("episodes_greater", str(min_episodes))
        if max_episodes is not None:
            self._add_or_replace_filter("episodes_lesser", str(max_episodes))
        return self

    def set_duration_range(self, min_duration: int = None, max_duration: int = None):
        if min_duration is not None:
            self._add_or_replace_filter("duration_greater", str(min_duration))
        if max_duration is not None:
            self._add_or_replace_filter("duration_lesser", str(max_duration))
        return self

    def set_chapters_range(self, min_chapters: int = None, max_chapters: int = None):
        if min_chapters is not None:
            self._add_or_replace_filter("chapters_greater", str(min_chapters))
        if max_chapters is not None:
            self._add_or_replace_filter("chapters_lesser", str(max_chapters))
        return self

    def set_year_range(self, min_year: int = None, max_year: int = None):
        if min_year is not None:
            self._add_or_replace_filter("startDate_greater", f"{min_year}0101")
        if max_year is not None:
            self._add_or_replace_filter("startDate_lesser", f"{max_year}1231")
        return self

    def set_adult(self, is_adult: bool = False):
        self._add_or_replace_filter("isAdult", "true" if is_adult else "false")
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

    def __hash__(self):
        return int(self.stable_hash(), 16)

    def stable_hash(self) -> str:
        filters_key = sorted(self.filters)

        # Convert to a deterministic string
        combined = json.dumps(filters_key, separators=(',', ':'))

        # Hash with SHA256
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()

    def __eq__(self, other):
        if not isinstance(other, SearchQueryBuilder):
            return NotImplemented
        return sorted(self.filters) == sorted(other.filters)

if __name__ == "__main__":
    media_query = MediaQueryBuilder()
    builder = SearchQueryBuilder().set_sort(MediaSort.TRENDING_DESC).set_search("one")
    query = builder.build(media_query)
    print(query)
