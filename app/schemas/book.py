from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

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