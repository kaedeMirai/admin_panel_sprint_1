
CREATE SCHEMA IF NOT EXISTS content;

-- Создание таблицы кинопроизведений
CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

-- Создание индекса
CREATE INDEX film_work_creation_date_idx ON content.film_work (creation_date);

-- Создание таблицы жанров
CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE INDEX genre_name_idx ON content.genre (name);

-- Создание таблицы участников фильма
CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE INDEX person_full_name_idx ON content.person (full_name);

-- Создание таблицы со связью многие ко многим для жанров и фильмов
CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role TEXT NOT NULL,
    created TIMESTAMP WITH TIME ZONE
);

CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work (film_work_id, person_id);

-- Создание таблицы со связью многие ко многим для участников фильма и фольмов
CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    created TIMESTAMP WITH TIME ZONE
);

CREATE UNIQUE INDEX film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id);


