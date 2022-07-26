CREATE DATABASE movies_database;

CREATE SCHEMA IF NOT EXISTS content;

ALTER ROLE app SET search_path TO content,public;

CREATE EXTENSION "uuid-ossp";

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE INDEX film_work_creation_date_idx ON content.film_work(creation_date);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role TEXT NOT NULL,
    created timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    created timestamp with time zone,

    constraint fk_genre
      foreign key(genre_id) 
	  references content.genre(genre_id)
      on delete cascade,
    
    constraint fk_film_work
      foreign key(film_work_id)
      references content.film_work(film_work_id)
      on delete cascade
);

ALTER TABLE content.genre_film_work
ADD CONSTRAINT fk_genre
FOREIGN KEY (genre_id)
REFERENCES content.genre(id)
ON DELETE CASCADE;

ALTER TABLE content.genre_film_work
ADD CONSTRAINT fk_genre
FOREIGN KEY (genre_id)
REFERENCES content.genre(id)
ON DELETE CASCADE;

CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work (film_work_id);
CREATE UNIQUE INDEX genre_film_work_idx ON content.genre_film_work (film_work_id);