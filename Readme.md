# AnilistPython

A Python client library for interacting with the AniList GraphQL API to fetch and search anime and manga data, including recommendations and relations.

## Features

- **Anime and Manga Fetching**: Retrieve detailed information about specific anime or manga by ID.
- **Search Functionality**: Search for anime or manga based on query strings with pagination support.
- **Recommendations**: Get recommendations for a specific media item.
- **Relations**: Fetch related media, such as sequels, prequels, or adaptations.
- **Customizable Queries**: Use query builders to customize GraphQL queries for media, search, and user activity.
- **Error Handling**: Robust error logging using `loguru` for GraphQL and transport errors.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dontknow492/AnilistPython.git
   cd AnilistPython
   ```

2. Install dependencies using a Python environment with Python >= 3.12:
   ```bash
   pip install -r requirements.txt
   ```

   Or, if using `pyproject.toml` with a tool like `poetry`:
   ```bash
   poetry install
   ```

## Usage

Below is an example of how to use the `AniListClient` to fetch and search anime/manga data.

```python
import asyncio
from AnilistPython import AniListClient, MediaQueryBuilder, SearchQueryBuilder, MediaQueryBuilderBase

async def main():
    # Initialize client
    anilist = AniListClient()

    # Create query builders
    media_query_builder = MediaQueryBuilder()
    search_query_builder = SearchQueryBuilder()
    relation_builder = MediaQueryBuilderBase()
    recommendation_builder = MediaQueryBuilderBase()

    # Fetch an anime by ID
    anime = await anilist.get_anime(media_id=1, builder=media_query_builder)
    print(anime)

    # Search for anime
    anime_list = await anilist.search_anime(
        builder=media_query_builder,
        filters=search_query_builder,
        query="One Piece",
        page=1,
        perpage=5
    )
    print(anime_list)

    # Get recommendations for a media
    recommendations = await anilist.get_recommendations(
        builder=recommendation_builder,
        media_id=1,
        page=1,
        perpage=5
    )
    print(recommendations)

    # Get relations for a media
    relations = await anilist.get_relations(
        builder=relation_builder,
        media_id=1
    )
    print(relations)

if __name__ == "__main__":
    asyncio.run(main())
```

## Project Structure

- **`anilistpython/`**: Main package directory.
  - `__init__.py`: Package initialization.
  - `client.py`: Core `AniListClient` implementation for API interactions.
  - `models/`: Data models for anime, manga, recommendations, and relations.
  - `queries/`: Query builders for constructing GraphQL queries.
  - `parser/`: Functions to parse GraphQL response data into models.
- **`schema.graphql`**: GraphQL schema file for the AniList API.
- **`pyproject.toml`**: Project configuration and dependencies.

## Dependencies

- `gql[all]>=3.5.3`: GraphQL client for Python with HTTPX transport.
- `loguru>=0.7.3`: Logging library for error handling.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.
6. Create Documentation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For issues or questions, please open an issue on GitHub or contact the maintainer.