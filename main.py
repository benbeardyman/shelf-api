from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from database import Base, engine
from routers import books, films

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shelf", description="Personal library tracker")

# API routes
app.include_router(books.router)
app.include_router(films.router)

# Serve React frontend (production)
STATIC_DIR = Path(__file__).parent.parent / "shelf-client" / "dist"

if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_spa(full_path: str):
        index = STATIC_DIR / "index.html"
        return FileResponse(index)
