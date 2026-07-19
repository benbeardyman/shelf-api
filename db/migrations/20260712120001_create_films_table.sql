-- migrate:up
CREATE TABLE IF NOT EXISTS films (
  id INTEGER PRIMARY KEY,
  title VARCHAR NOT NULL,
  director VARCHAR,
  year INTEGER,
  genre VARCHAR,
  type VARCHAR NOT NULL,
  date_watched DATE,
  rating INTEGER,
  notes TEXT
);

CREATE INDEX IF NOT EXISTS ix_films_id ON films(id);

-- migrate:down
DROP TABLE IF EXISTS films;
