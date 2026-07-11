from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Film
from schemas import FilmCreate, FilmUpdate, FilmOut

router = APIRouter(prefix="/api/films", tags=["films"])


@router.get("/", response_model=List[FilmOut])
def list_films(db: Session = Depends(get_db)):
    return db.query(Film).order_by(Film.date_watched.desc()).all()


@router.get("/{film_id}", response_model=FilmOut)
def get_film(film_id: int, db: Session = Depends(get_db)):
    film = db.get(Film, film_id)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film


@router.post("/", response_model=FilmOut, status_code=201)
def create_film(payload: FilmCreate, db: Session = Depends(get_db)):
    film = Film(**payload.model_dump())
    db.add(film)
    db.commit()
    db.refresh(film)
    return film


@router.patch("/{film_id}", response_model=FilmOut)
def update_film(film_id: int, payload: FilmUpdate, db: Session = Depends(get_db)):
    film = db.get(Film, film_id)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(film, key, value)
    db.commit()
    db.refresh(film)
    return film


@router.delete("/{film_id}", status_code=204)
def delete_film(film_id: int, db: Session = Depends(get_db)):
    film = db.get(Film, film_id)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    db.delete(film)
    db.commit()
