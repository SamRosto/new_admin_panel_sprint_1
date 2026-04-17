class MoviesTransformer:
    def transform(self, rows: list[dict]) -> list[dict]:
        docs = []
        for r in rows:
            directors = r.get("directors", []) or []
            actors = r.get("actors", []) or []
            writers = r.get("writers", []) or []
            genres = r.get("genres", []) or []

            docs.append(
                {
                    "id": str(r["id"]),
                    "imdb_rating": r.get("rating"),
                    "genres": [g["name"] for g in genres],
                    "title": r.get("title"),
                    "description": r.get("description"),
                    "directors_names": [p["name"] for p in directors],
                    "actors_names": [p["name"] for p in actors],
                    "writers_names": [p["name"] for p in writers],
                    "directors": directors,
                    "actors": actors,
                    "writers": writers,
                }
            )
        return docs
