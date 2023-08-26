import uuid
from datetime import datetime, date
from dataclasses import dataclass
from data_from_sqlite import data_from_sqlite
from data_to_postgre import insert_data_to_postgres


@dataclass
class Genre:
    id: uuid.uuid4
    name: str
    description: str
    created: datetime
    modified: datetime


@dataclass
class FilmWork:
    id: uuid.uuid4
    title: str
    description: str
    creation_date: date
    file_path: str
    rating: float
    type: str
    created: datetime
    modified: datetime


@dataclass
class Person:
    id: uuid.uuid4
    full_name: str
    created: datetime
    modified: datetime


@dataclass
class PersonFilmWork:
    id: uuid.uuid4
    film_work_id: uuid.uuid4
    person_id: uuid.uuid4
    role: str
    created: datetime


@dataclass
class GenreFilmWork:
    id: uuid.uuid4
    film_work_id: uuid.uuid4
    genre_id: uuid.uuid4
    created: datetime


if __name__ == '__main__':
    db_path = r'./sqlite_to_postgres/db.sqlite'
    psql_conn_data = {
        'dbname': 'movies_database',
        'user': 'app',
        'password': '123qwe',
        'host': 'localhost',
        'port': 54320,
        'options': '-c search_path=content',
        'client_encoding': 'utf-8',
    }

    table_mapping = {
        'genre': Genre,
        'film_work': FilmWork,
        'person': Person,
        'person_film_work': PersonFilmWork,
        'genre_film_work': GenreFilmWork
    }

    for table_name, dataclass_type in table_mapping.items():
        from_sqlite = data_from_sqlite(db_path, table_name, dataclass_type)
        column_names = from_sqlite[1]
        data = from_sqlite[0]
        insert_data_to_postgres(data, table_name, column_names, psql_conn_data)
