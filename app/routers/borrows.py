from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import crud, database, schemas

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API route to get all borrows
@router.get("/borrows/", response_model=List[schemas.BorrowOut])
def read_borrows(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    borrows = crud.get_borrows(db, skip=skip, limit=limit)
    return borrows

# API route to create a new borrow
@router.post("/borrows/", response_model=schemas.BorrowOut)
def create_borrow(borrow: schemas.BorrowCreate, db: Session = Depends(get_db)):
    return crud.create_borrow(db=db, borrow=borrow)

# API route to update a borrow by ID
@router.put("/borrows/{borrow_id}", response_model=schemas.BorrowOut)
def update_borrow(borrow_id: int, borrow_update: schemas.BorrowUpdate, db: Session = Depends(get_db)):
    borrow = crud.update_borrow(db=db, borrow_id=borrow_id, borrow_update=borrow_update)
    if borrow is None:
        raise HTTPException(status_code=404, detail="Borrow not found")
    return borrow

# API route to delete a borrow by ID
@router.delete("/borrows/{borrow_id}", response_model=schemas.BorrowOut)
def delete_borrow(borrow_id: int, db: Session = Depends(get_db)):
    borrow = crud.delete_borrow(db=db, borrow_id=borrow_id)
    if borrow is None:
        raise HTTPException(status_code=404, detail="Borrow not found")
    return borrow
