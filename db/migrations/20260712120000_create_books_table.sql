-- migrate:up
CREATE TABLE books (
  id INTEGER PRIMARY KEY,
  title VARCHAR NOT NULL,
  author VARCHAR NOT NULL,
  year INTEGER,
  genre VARCHAR,
  date_read DATE,
  rating INTEGER,
  notes TEXT
);

CREATE INDEX ix_books_id ON books(id);

-- migrate:down
DROP TABLE IF EXISTS books;
