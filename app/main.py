from app.routers import books
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.db.database import Base, engine
from app.routers import films
from app.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Shelf", description="Personal library tracker")

logger.info("FastAPI application created: Shelf - Personal library tracker")

# API routes
logger.debug("Registering books router")
app.include_router(books.router)
logger.debug("Registering films router")
app.include_router(films.router)
logger.info("All API routes registered successfully")

# Serve React frontend (production)
STATIC_DIR = Path(__file__).parent.parent / "shelf-client" / "dist"

if STATIC_DIR.exists():
    logger.info(f"React frontend found at {STATIC_DIR}, mounting static files")
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_spa(full_path: str):
        logger.debug(f"Serving SPA for path: {full_path}")
        index = STATIC_DIR / "index.html"
        return FileResponse(index)
else:
    logger.warning(f"React frontend not found at {STATIC_DIR}. Static files will not be served.")
