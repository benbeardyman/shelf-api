-- migrate:up
CREATE TABLE films (
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

CREATE INDEX ix_films_id ON films(id);

-- migrate:down
DROP TABLE IF EXISTS films;
