import psycopg2
from psycopg2.extras import RealDictCursor


class PostgresExtractor:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.conn = None
        self._connect()

    def _connect(self):
        self.conn = psycopg2.connect(self.dsn, cursor_factory=RealDictCursor)
        self.conn.autocommit = True

    def _fetchall(self, query: str, params: dict):
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()
        except psycopg2.OperationalError:
            self._connect()
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()

    def fetch_film_work_batch(self, ts: str, obj_id: str, limit: int):
        return self._fetchall(
            """
            SELECT id, modified
            FROM content.film_work
            WHERE (modified, id) > (%(ts)s, %(obj_id)s::uuid)
            ORDER BY modified, id
            LIMIT %(limit)s;
            """,
            {"ts": ts, "obj_id": obj_id, "limit": limit},
        )

    def fetch_person_batch(self, ts: str, obj_id: str, limit: int):
        return self._fetchall(
            """
            SELECT id, modified
            FROM content.person
            WHERE (modified, id) > (%(ts)s, %(obj_id)s::uuid)
            ORDER BY modified, id
            LIMIT %(limit)s;
            """,
            {"ts": ts, "obj_id": obj_id, "limit": limit},
        )

    def fetch_genre_batch(self, ts: str, obj_id: str, limit: int):
        return self._fetchall(
            """
            SELECT id, modified
            FROM content.genre
            WHERE (modified, id) > (%(ts)s, %(obj_id)s::uuid)
            ORDER BY modified, id
            LIMIT %(limit)s;
            """,
            {"ts": ts, "obj_id": obj_id, "limit": limit},
        )

    def film_ids_by_person_ids(self, person_ids: list[str]):
        if not person_ids:
            return []
        rows = self._fetchall(
            """
            SELECT DISTINCT film_work_id AS id
            FROM content.person_film_work
            WHERE person_id = ANY(%(person_ids)s::uuid[]);
            """,
            {"person_ids": person_ids},
        )
        return [str(r["id"]) for r in rows]

    def film_ids_by_genre_ids(self, genre_ids: list[str]):
        if not genre_ids:
            return []
        rows = self._fetchall(
            """
            SELECT DISTINCT film_work_id AS id
            FROM content.genre_film_work
            WHERE genre_id = ANY(%(genre_ids)s::uuid[]);
            """,
            {"genre_ids": genre_ids},
        )
        return [str(r["id"]) for r in rows]

    def fetch_movies_payload(self, film_ids: list[str]):
        if not film_ids:
            return []
        return self._fetchall(
            """
            SELECT
                fw.id,
                fw.title,
                fw.description,
                fw.rating,
                fw.modified,
                COALESCE(
                    json_agg(DISTINCT jsonb_build_object('id', g.id, 'name', g.name))
                    FILTER (WHERE g.id IS NOT NULL), '[]'
                ) AS genres,
                COALESCE(
                    json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
                    FILTER (WHERE p.id IS NOT NULL AND pfw.role = 'actor'), '[]'
                ) AS actors,
                COALESCE(
                    json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
                    FILTER (WHERE p.id IS NOT NULL AND pfw.role = 'writer'), '[]'
                ) AS writers,
                COALESCE(
                    json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
                    FILTER (WHERE p.id IS NOT NULL AND pfw.role = 'director'), '[]'
                ) AS directors
            FROM content.film_work fw
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            WHERE fw.id = ANY(%(film_ids)s::uuid[])
            GROUP BY fw.id
            ORDER BY fw.modified, fw.id;
            """,
            {"film_ids": film_ids},
        )
