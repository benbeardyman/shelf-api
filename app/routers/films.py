from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.film import Film
from app.schemas.film import FilmCreate, FilmUpdate, FilmOut
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/films", tags=["films"])


@router.get("/", response_model=List[FilmOut])
def list_films(db: Session = Depends(get_db)):
    logger.info("Fetching all films")
    films = db.query(Film).order_by(Film.date_watched.desc()).all()
    logger.info(f"Retrieved {len(films)} {'films' if len(films) > 1 else 'film'}")
    return films


@router.get("/{film_id}", response_model=FilmOut)
def get_film(film_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching film with ID: {film_id}")
    film = db.get(Film, film_id)
    if not film:
        logger.warning(f"Film not found with ID: {film_id}")
        raise HTTPException(status_code=404, detail="Film not found")
    logger.info(f"Successfully retrieved film: {film.title}")
    return film


@router.post("/", response_model=FilmOut, status_code=201)
def create_film(payload: FilmCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating new film: {payload.title}")
    try:
        film = Film(**payload.model_dump())
        db.add(film)
        db.commit()
        db.refresh(film)
        logger.info(f"Film created successfully with ID: {film.id} - {film.title}")
        return film
    except Exception as e:
        logger.error(f"Error creating film: {str(e)}")
        db.rollback()
        raise


@router.patch("/{film_id}", response_model=FilmOut)
def update_film(film_id: int, payload: FilmUpdate, db: Session = Depends(get_db)):
    logger.info(f"Updating film with ID: {film_id}")
    film = db.get(Film, film_id)
    if not film:
        logger.warning(f"Film not found for update with ID: {film_id}")
        raise HTTPException(status_code=404, detail="Film not found")
    try:
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(film, key, value)
        db.commit()
        db.refresh(film)
        logger.info(f"Film updated successfully with ID: {film_id}")
        return film
    except Exception as e:
        logger.error(f"Error updating film {film_id}: {str(e)}")
        db.rollback()
        raise


@router.delete("/{film_id}", status_code=204)
def delete_film(film_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting film with ID: {film_id}")
    film = db.get(Film, film_id)
    if not film:
        logger.warning(f"Film not found for deletion with ID: {film_id}")
        raise HTTPException(status_code=404, detail="Film not found")
    try:
        db.delete(film)
        db.commit()
        logger.info(f"Film deleted successfully with ID: {film_id}")
    except Exception as e:
        logger.error(f"Error deleting film {film_id}: {str(e)}")
        db.rollback()
        raise
