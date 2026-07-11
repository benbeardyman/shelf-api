from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


# --- Books ---

class BookCreate(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    genre: Optional[str] = None
    date_read: Optional[date] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    notes: Optional[str] = None


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    date_read: Optional[date] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    notes: Optional[str] = None


class BookOut(BookCreate):
    id: int

    model_config = {"from_attributes": True}


# --- Films ---

class FilmCreate(BaseModel):
    title: str
    director: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    date_watched: Optional[date] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    notes: Optional[str] = None


class FilmUpdate(BaseModel):
    title: Optional[str] = None
    director: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    date_watched: Optional[date] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    notes: Optional[str] = None


class FilmOut(FilmCreate):
    id: int

    model_config = {"from_attributes": True}
