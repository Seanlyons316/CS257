CREATE TABLE authors (
    id integer NOT NULL,
    surname text,
    given_name text,
    birth_year integer,
    death_year integer
);

CREATE TABLE books (
    id integer NOT NULL,
    title text,
    publication_year integer
);

CREATE TABLE books_authors (
    book_id integer,
    author_id integer
);

