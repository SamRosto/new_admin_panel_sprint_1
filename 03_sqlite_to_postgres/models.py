"""Models."""
import uuid
from dataclasses import dataclass
import typing as t
import datetime as dt
from enum import Enum


class MovieType(Enum):
    movie = 'movie'
    tv_series = 'tv_show'
    

@dataclass
class FilmWork:
    id: uuid.UUID
    title: str
    description: str
    creation_date: t.Optional[dt.datetime]
    rating: float
    type: MovieType 
    updated_at: str
    created_at: str
    file_path: t.Optional[str | None]
    

@dataclass
class Genre:
    id: uuid.uuid4
    name: str
    description: t.Optional[str | None]
    created_at: str
    updated_at: str


@dataclass
class Person:
    id: uuid.uuid4
    full_name: str
    created_at: str
    updated_at: str


@dataclass
class GenreFilmWork:
    id:uuid.uuid4
    film_work_id: uuid.uuid4
    genre_id: uuid.uuid4
    created_at: str


@dataclass
class PersonFilmWork:
    id: uuid.uuid4
    film_work_id: uuid.uuid4
    person_id: uuid.uuid4
    role: str
    created_at: str
