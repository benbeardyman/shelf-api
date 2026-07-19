-- migrate:up
CREATE TABLE IF NOT EXISTS books (
  id INTEGER PRIMARY KEY,
  title VARCHAR NOT NULL,
  author VARCHAR NOT NULL,
  year INTEGER,
  genre VARCHAR,
  date_read DATE,
  rating INTEGER,
  notes TEXT
);

CREATE INDEX IF NOT EXISTS ix_books_id ON books(id);

-- migrate:down
DROP TABLE IF EXISTS books;
