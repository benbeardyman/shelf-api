# shelf-api

REST API for Shelf — a personal library tracker for books and films. Built with FastAPI and SQLite. Designed to run on a Raspberry Pi Zero W.

## Requirements

- Python 3.8+
- No external database server — SQLite is built into Python

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running locally

```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

Interactive API docs (Swagger UI) are available at `http://localhost:8000/docs`.

## Project structure

```
shelf-api/
├── app/
│   ├── __init__.py
│   ├── main.py      # Application entry point, router registration, static file serving
│   ├── database.py  # SQLAlchemy engine, session factory, Base class
│   ├── logger.py    # Logging configuration
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── books.py # CRUD routes for /api/books
│   │   └── films.py # CRUD routes for /api/films
|   ├── models/
│   │   ├── __init__.py
│   │   ├── book.py # ORM model for books
│   │   └── film.py # ORM model for films
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── book.py # Pydantic schemas for books
│   │   └── film.py # Pydantic schemas for films
│   └── db/
│       ├── __init__.py
│       └── database.py
├── db/
│   ├── migrations/  # Database migrations (dbmate)
│   │   ├── 20260719120000_create_books_table.sql
│   │   └── 20260719120001_create_films_table.sql
│   └── schema.sql   # Auto-generated complete schema (commit to git for diffs)
├── .env             # Environment variables (DATABASE_URL)
├── requirements.txt
└── shelf.db         # SQLite database file (created automatically on first run)
```

## Database

SQLite is used as the database. The file `shelf.db` is created automatically in the `shelf-api/` directory when migrations are applied. The database file is excluded from version control.

### Migrations

This project uses **dbmate** for database migrations. Migrations are plain SQL files stored in `db/migrations/` and tracked in the database's `schema_migrations` table.

#### Viewing migration status

```bash
npx dbmate status
```

Output shows which migrations have been applied:
```
[X] 20260719120000_create_books_table.sql
[X] 20260719120001_create_films_table.sql

Applied: 2
Pending: 0
```

#### Applying migrations

```bash
npx dbmate up
```

This creates the database and applies any pending migrations. The `schema_migrations` table is automatically created to track applied migrations.

#### Creating a new migration

```bash
npx dbmate new add_column_to_books
```

This generates a new migration file with `-- migrate:up` and `-- migrate:down` sections. Edit the file to add your SQL:

```sql
-- migrate:up
ALTER TABLE books ADD COLUMN status TEXT;

-- migrate:down
ALTER TABLE books DROP COLUMN status;
```

#### Rolling back migrations

```bash
npx dbmate rollback
```

This rolls back the most recently applied migration.

#### Schema dump

After running migrations, a complete schema dump is saved to `db/schema.sql`. Commit this file to version control to track schema changes in diffs.

Back up the database file:

```bash
cp shelf.db shelf.db.bak
```

## API endpoints

| Method | Path              | Description       |
| ------ | ----------------- | ----------------- |
| GET    | `/api/books/`     | List all books    |
| POST   | `/api/books/`     | Add a book        |
| GET    | `/api/books/{id}` | Get a single book |
| PATCH  | `/api/books/{id}` | Update a book     |
| DELETE | `/api/books/{id}` | Delete a book     |
| GET    | `/api/films/`     | List all films    |
| POST   | `/api/films/`     | Add a film        |
| GET    | `/api/films/{id}` | Get a single film |
| PATCH  | `/api/films/{id}` | Update a film     |
| DELETE | `/api/films/{id}` | Delete a film     |

### Book fields

| Field     | Type              | Required |
| --------- | ----------------- | -------- |
| title     | string            | yes      |
| author    | string            | yes      |
| year      | integer           | no       |
| genre     | string            | no       |
| date_read | date (YYYY-MM-DD) | no       |
| rating    | integer (1–5)     | no       |
| notes     | string            | no       |

### Film fields

| Field        | Type              | Required |
| ------------ | ----------------- | -------- |
| title        | string            | yes      |
| director     | string            | no       |
| year         | integer           | no       |
| genre        | string            | no       |
| type         | string            | yes      |
| date_watched | date (YYYY-MM-DD) | no       |
| rating       | integer (1–5)     | no       |
| notes        | string            | no       |

## Serving the frontend (production)

In production the API also serves the built frontend static files. Place the `shelf-client` build output at `../shelf-client/dist/` relative to this directory and the API will serve it automatically. All non-API routes return `index.html` to support client-side routing.

## Deployment on Raspberry Pi Zero W

### First-time setup on the Pi

```bash
# On the Pi
cd ~/shelf/shelf-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### systemd service

Install the service so the app starts on boot and restarts on failure:

```bash
sudo cp ~/shelf/shelf.service /etc/systemd/system/shelf.service
sudo systemctl daemon-reload
sudo systemctl enable shelf
sudo systemctl start shelf
```

Check status:

```bash
sudo systemctl status shelf
journalctl -u shelf -f   # live logs
```

### Subsequent deploys

Run from your development machine using the deploy script in the root of the monorepo:

```bash
./deploy.sh
# or with a specific IP:
./deploy.sh 192.168.1.42
```

The deploy script automatically:
1. Builds the frontend
2. Syncs migration files to the Pi
3. Downloads the dbmate binary on the Pi
4. Runs pending migrations
5. Restarts the service

Any new migrations added to `db/migrations/` will be applied during deployment.

## Dependencies

| Package    | Purpose                              |
| ---------- | ------------------------------------ |
| fastapi    | Web framework                        |
| uvicorn    | ASGI server                          |
| sqlalchemy | ORM and query builder                |
| dbmate     | Database migrations (dev dependency) |
| pydantic   | Request/response validation          |
