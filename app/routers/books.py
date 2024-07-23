from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import crud, models, database

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API route to get all books
@router.get("/books/", response_model=List[models.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

# API route to get a book by ID
@router.get("/books/{book_id}", response_model=models.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# API route to create a new book
@router.post("/books/", response_model=models.Book)
def create_book(book: models.Book, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)

# API route to update a book by ID
@router.put("/books/{book_id}", response_model=models.Book)
def update_book(book_id: int, title: str = None, author: str = None, pub_date: str = None, l_code: int = None, db: Session = Depends(get_db)):
    book = crud.update_book(db=db, book_id=book_id, title=title, author=author, pub_date=pub_date, l_code=l_code)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# API route to delete a book by ID
@router.delete("/books/{book_id}", response_model=models.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.delete_book(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
