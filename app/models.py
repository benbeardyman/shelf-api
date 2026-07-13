from sqlalchemy import Column, Integer, String, Date, Text
from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer)
    genre = Column(String)
    date_read = Column(Date)
    rating = Column(Integer)  # 1-5
    notes = Column(Text)


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    director = Column(String)
    year = Column(Integer)
    genre = Column(String)
    type = Column(String, nullable=False)
    date_watched = Column(Date)
    rating = Column(Integer)  # 1-5
    notes = Column(Text)
