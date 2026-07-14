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
│       ├── database.py
│       ├── migrate.py
├── requirements.txt
└── shelf.db         # SQLite database file (created automatically on first run)
```

## Database

SQLite is used as the database. The file `shelf.db` is created automatically in the `shelf-api/` directory the first time the application starts. No setup or migration step is required for a fresh install.

The database file is excluded from version control. Back it up by copying the file:

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

## Dependencies

| Package    | Purpose                            |
| ---------- | ---------------------------------- |
| fastapi    | Web framework                      |
| uvicorn    | ASGI server                        |
| sqlalchemy | ORM and query builder              |
| alembic    | Schema migrations (for future use) |
| pydantic   | Request/response validation        |
