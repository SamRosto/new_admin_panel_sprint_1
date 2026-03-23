import os
import sqlite3
from dataclasses import asdict
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor

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
def sqlite_connection(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def postgres_connection(dsn_params: dict):
    conn = psycopg2.connect(**dsn_params, cursor_factory=DictCursor)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@contextmanager
def db_connections(db_path: str, dsn_params: dict):
    with sqlite_connection(db_path) as sqlite_conn, postgres_connection(dsn_params) as pg_conn:
        yield sqlite_conn, pg_conn


def load_all_data(sqlite_conn: sqlite3.Connection, pg_conn):
    dataclass_objects = {
        "film_work": FilmWork,
        "person_film_work": PersonFilmWork,
        "genre": Genre,
        "person": Person,
        "genre_film_work": GenreFilmWork,
    }

    cur = sqlite_conn.cursor()
    for table_name, dc_cls in dataclass_objects.items():
        data = SQLiteLoader(cur, table_name).load_data()
        data_objects = [dc_cls(**dict(row)) for row in data]
        to_dicts = [asdict(obj) for obj in data_objects]

        PostgresSaver(pg_conn, table_name).save_data(to_dicts)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "db.sqlite")

    with db_connections(db_path, dsn) as (sqlite_conn, pg_conn):
        load_all_data(sqlite_conn, pg_conn)