import sqlite3
import os

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from dataclasses import asdict
from contextlib import contextmanager

from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from sqlite_worker import SQLiteLoader
from pg_worker import PostgresSaver
import settings


dsn = {
    "dbname": settings.DBNAME,
    "user": settings.USER,
    "password": settings.PASSWORD,
    "host": settings.HOST,
    "port": settings.PORT,
}


@contextmanager
class Connection:
    def __init__(self, pg_conn: _connection, sqlite_conn: sqlite3.Connection) -> None:
        self.pg_conn = pg_conn
        self.sqlite_conn = sqlite_conn
        self.dataclass_objects = {
            "film_work": FilmWork,
            "person_film_work": PersonFilmWork,
            "genre": Genre,
            "person": Person,
            "genre_film_work": GenreFilmWork,
        }

        def __enter__(self):
            self.sqlite_conn.row_factory = sqlite3.Row
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if hasattr(self, "pg_conn"):
                self.pg_conn.close()
            if hasattr(self, "sqlite_conn"):
                self.sqlite_conn.close()

        # with self.sqlite_conn:
        def load_all_data(self):
            cur = self.sqlite_conn.cursor()

            def load_data_sqlite(k):
                sqlite_loader = SQLiteLoader(cur, k)
                return sqlite_loader.load_data()

            def create_object(data, v):
                o = [v(**dict(field)) for field in data]
                return o

            def make_dicts(lst):
                for obj in lst:
                    dataclass_to_dict = [asdict(obj) for obj in lst]
                    return dataclass_to_dict

            for k, v in self.dataclass_objects.items():
                data = load_data_sqlite(k)
                data_objects = create_object(data, v)
                to_dicts = make_dicts(data_objects)

                # Load to Postgres in the loop
                saver_pg = PostgresSaver(self.pg_conn, k)
                saver_pg.save_data(to_dicts)


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "db.sqlite")

    with (
        sqlite3.connect(db_path) as sqlite_conn,
        psycopg2.connect(**dsn, cursor_factory=DictCursor) as pg_conn,
    ):
        with Connection(sqlite_conn=sqlite_conn, pg_conn=pg_conn) as conn:
            conn.load_all_data()
