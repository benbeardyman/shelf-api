from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Book
from app.schemas import BookCreate, BookUpdate, BookOut
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/books", tags=["books"])


@router.get("/", response_model=List[BookOut])
def list_books(db: Session = Depends(get_db)):
    logger.info("Fetching all books")
    books = db.query(Book).order_by(Book.date_read.desc()).all()
    logger.info(f"Retrieved {len(books)} {'books' if len(books) > 1 else 'book'}")
    return books


@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching book with ID: {book_id}")
    book = db.get(Book, book_id)
    if not book:
        logger.warning(f"Book not found with ID: {book_id}")
        raise HTTPException(status_code=404, detail="Book not found")
    logger.info(f"Successfully retrieved book: {book.title}")
    return book


@router.post("/", response_model=BookOut, status_code=201)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating new book: {payload.title}")
    try:
        book = Book(**payload.model_dump())
        db.add(book)
        db.commit()
        db.refresh(book)
        logger.info(f"Book created successfully with ID: {book.id} - {book.title}")
        return book
    except Exception as e:
        logger.error(f"Error creating book: {str(e)}")
        db.rollback()
        raise


@router.patch("/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    logger.info(f"Updating book with ID: {book_id}")
    book = db.get(Book, book_id)
    if not book:
        logger.warning(f"Book not found for update with ID: {book_id}")
        raise HTTPException(status_code=404, detail="Book not found")
    try:
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(book, key, value)
        db.commit()
        db.refresh(book)
        logger.info(f"Book updated successfully with ID: {book_id}")
        return book
    except Exception as e:
        logger.error(f"Error updating book {book_id}: {str(e)}")
        db.rollback()
        raise


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting book with ID: {book_id}")
    book = db.get(Book, book_id)
    if not book:
        logger.warning(f"Book not found for deletion with ID: {book_id}")
        raise HTTPException(status_code=404, detail="Book not found")
    try:
        db.delete(book)
        db.commit()
        logger.info(f"Book deleted successfully with ID: {book_id}")
    except Exception as e:
        logger.error(f"Error deleting book {book_id}: {str(e)}")
        db.rollback()
        raise
