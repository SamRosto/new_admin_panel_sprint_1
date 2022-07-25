"""Postgres worker."""
from dataclasses import dataclass
from psycopg2.extensions import connection
from psycopg2.extras import execute_batch


queries = {
    'film_work':"""insert into content.film_work
        (id, title, description, creation_date, rating, type, created, modified, file_path)
        values(%(id)s, %(title)s, %(description)s, %(creation_date)s, %(rating)s, 
        %(type)s, %(created_at)s, %(updated_at)s, %(file_path)s)
        on conflict (id) do nothing;""",

    'person_film_work': """insert into content.person_film_work
        (id, film_work_id, person_id, role, created)
        values(%(id)s, %(film_work_id)s, %(person_id)s, %(role)s, %(created_at)s)
        on conflict (film_work_id, person_id) do nothing;""",

    'genre': """insert into content.genre
        (id, name, description, created, modified)
        values(%(id)s, %(name)s, %(description)s, %(created_at)s, %(updated_at)s)
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
        cur = self.conn.cursor()
        PAGE_SIZE = 50
        query = queries[self.table_name]
        execute_batch(cur, query, data, page_size=PAGE_SIZE)

        self.conn.commit()
        

