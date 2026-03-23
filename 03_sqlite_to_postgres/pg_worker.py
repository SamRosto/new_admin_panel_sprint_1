"""Postgres worker."""
from dataclasses import dataclass
from psycopg2.extensions import connection
from psycopg2.extras import execute_batch


queries = {
    'film_work':"""insert into content.film_work
        (id, title, description, creation_date, rating, type, created, modified, file_path)
        values(
            %(id)s,
            COALESCE(%(title)s, ''),
            COALESCE(%(description)s, ''),
            COALESCE(%(creation_date)s, (%(created_at)s)::date),
            COALESCE(%(rating)s, 0),
            COALESCE(%(type)s, 'movie'),
            %(created_at)s,
            %(updated_at)s,
            COALESCE(%(file_path)s, '')
        )
        on conflict (id) do nothing;""",

    'person_film_work': """insert into content.person_film_work
        (id, film_work_id, person_id, role, creation_date)
        values(%(id)s, %(film_work_id)s, %(person_id)s, %(role)s, %(created_at)s)
        on conflict (id) do nothing;""",

    'genre': """insert into content.genre
        (id, name, description, created, modified)
        values(%(id)s, %(name)s, COALESCE(%(description)s, ''), %(created_at)s, %(updated_at)s)
        on conflict (id) do nothing;""",

    'person': """insert into content.person
        (id, full_name, created, modified)
        values(%(id)s, %(full_name)s, %(created_at)s, %(updated_at)s)
        on conflict (id) do nothing;""",

    'genre_film_work': """insert into content.genre_film_work
        (id, genre_id, film_work_id, created)
        values(%(id)s, %(genre_id)s, %(film_work_id)s, %(created_at)s)
        on conflict (id) do nothing;""",
}


@dataclass
class PostgresSaver:
    conn: connection
    table_name: str

    def save_data(self, data):
        if not data:
            return

        cur = self.conn.cursor()
        PAGE_SIZE = 50
        query = queries[self.table_name]
        # execute_batch(cur, query, data, page_size=PAGE_SIZE)

        # self.conn.commit()
        try:
            execute_batch(cur, query, data, page_size=50)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Table: {self.table_name}")
            print(f"Sample keys: {list(data[0].keys())}")
            print(f"Error: {e}")
            raise
        finally:
            cur.close()
        

