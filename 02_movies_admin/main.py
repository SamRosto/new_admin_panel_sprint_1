import random
import uuid
import psycopg2
import config.settings as settings

from datetime import datetime
from faker import Faker
from psycopg2.extras import execute_batch

fake = Faker()

dsn = {
    'dbname': settings.DB_NAME,
    'user': settings.DB_USER,
    'password': settings.DB_PASSWORD,
    'host': 'localhost',
    'port': 5432,
    # 'options': '-c search_path=content',
}

PERSONS_COUNT = 100_000
PAGE_SIZE = 5_000

now = datetime.utcnow()

# Establish conn
with psycopg2.connect(**dsn) as conn, conn.cursor() as cur:
    # Fill person table
    persons_ids = [str(uuid.uuid4()) for _ in range(PERSONS_COUNT)]
    query = 'INSERT INTO content.person (id, full_name, created, modified) VALUES (%s, %s, %s, %s)'
    data = [(pk, fake.last_name(), now, now) for pk in persons_ids]
    execute_batch(cur, query, data, page_size=PAGE_SIZE)
    conn.commit()

    # Fill PersonFilmWork
    person_film_work_data = []
    roles = ['actor', 'director', 'producer']

    cur.execute('SELECT id FROM content.film_work')
    film_work_ids = [data[0] for data in cur.fetchall()] 

    for film_work_id in film_work_ids:
        for person_id in random.sample(persons_ids, 5):
            role = random.choice(roles)
            person_film_work_data.append((str(uuid.uuid4()), film_work_id, person_id, role, now))
    
    query = 'INSERT INTO content.person_film_work (id, film_work_id, person_id, role, created) VALUES (%s, %s, %s, %s, %s)'
    execute_batch(cur, query, person_film_work_data, page_size=PAGE_SIZE)
    conn.commit()

                                    

    
