from dataclasses import dataclass
import sqlite3


queries = {
    'film_work': 'select * from film_work;',
    'person_film_work': 'select * from person_film_work;',
    'genre': 'select * from genre;',
    'person': 'select * from person;',
    'genre_film_work': 'select * from genre_film_work;',
}

@dataclass
class SQLiteLoader:
    cur: sqlite3.Connection.cursor
    table_name: str

    def load_data(self):
        query = queries[self.table_name]
        self.cur.execute(query)

        data = []

        while True:
            records = self.cur.fetchmany(size=50)
            if records:
                for row in records:
                    data.append(dict(row))
            else:
                break
        
        return data
