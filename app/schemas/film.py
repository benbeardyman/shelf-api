from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class FilmType(str, Enum):
    FILM = "Film"
    TV = "TV"

class FilmCreate(BaseModel):
    title: str
    director: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    date_watched: Optional[date] = None
    type: FilmType
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    notes: Optional[str] = None


class FilmUpdate(BaseModel):
    title: Optional[str] = None
    director: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    date_watched: Optional[date] = None
    type: Optional[FilmType] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    notes: Optional[str] = None


class FilmOut(FilmCreate):
    id: int

    model_config = {"from_attributes": True}

