from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import crud, models, database, schemas

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API route to get all books
@router.get("/books/", response_model=List[schemas.BookOut])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

# API route to get a book by ID
@router.get("/books/{book_id}", response_model=schemas.BookOut)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# API route to create a new book
@router.post("/books/", response_model=schemas.BookOut)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)

# API route to update a book by ID
@router.put("/books/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    book = crud.update_book(db=db, book_id=book_id, book_update=book_update)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# API route to delete a book by ID
@router.delete("/books/{book_id}", response_model=schemas.BookOut)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.delete_book(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
