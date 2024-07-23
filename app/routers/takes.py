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

# API route to get all takes
@router.get("/takes/", response_model=List[models.Takes])
def read_takes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    takes = crud.get_takes(db, skip=skip, limit=limit)
    return takes

# API route to get a take by ID
@router.get("/takes/{take_id}", response_model=models.Takes)
def read_take(take_id: int, db: Session = Depends(get_db)):
    take = crud.get_take(db, take_id=take_id)
    if take is None:
        raise HTTPException(status_code=404, detail="Take not found")
    return take

# API route to create a new take
@router.post("/takes/", response_model=models.Takes)
def create_take(take: models.Takes, db: Session = Depends(get_db)):
    return crud.create_take(db=db, take=take)

# API route to update a take by ID
@router.put("/takes/{take_id}", response_model=models.Takes)
def update_take(take_id: int, student_id: int = None, course_code: int = None, year: int = None, semester: str = None, db: Session = Depends(get_db)):
    take = crud.update_take(db=db, take_id=take_id, student_id=student_id, course_code=course_code, year=year, semester=semester)
    if take is None:
        raise HTTPException(status_code=404, detail="Take not found")
    return take

# API route to delete a take by ID
@router.delete("/takes/{take_id}", response_model=models.Takes)
def delete_take(take_id: int, db: Session = Depends(get_db)):
    take = crud.delete_take(db=db, take_id=take_id)
    if take is None:
        raise HTTPException(status_code=404, detail="Take not found")
    return take
