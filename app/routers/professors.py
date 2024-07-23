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

# API route to get all professors
@router.get("/professors/", response_model=List[models.Professor])
def read_professors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    professors = crud.get_professors(db, skip=skip, limit=limit)
    return professors

# API route to get a professor by ID
@router.get("/professors/{professor_id}", response_model=models.Professor)
def read_professor(professor_id: int, db: Session = Depends(get_db)):
    professor = crud.get_professor(db, professor_id=professor_id)
    if professor is None:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor

# API route to create a new professor
@router.post("/professors/", response_model=models.Professor)
def create_professor(professor: models.Professor, db: Session = Depends(get_db)):
    return crud.create_professor(db=db, professor=professor)

# API route to update a professor by ID
@router.put("/professors/{professor_id}", response_model=models.Professor)
def update_professor(professor_id: int, first_name: str = None, last_name: str = None, phone: str = None, department_id: int = None, db: Session = Depends(get_db)):
    professor = crud.update_professor(db=db, professor_id=professor_id, first_name=first_name, last_name=last_name, phone=phone, department_id=department_id)
    if professor is None:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor

# API route to delete a professor by ID
@router.delete("/professors/{professor_id}", response_model=models.Professor)
def delete_professor(professor_id: int, db: Session = Depends(get_db)):
    professor = crud.delete_professor(db=db, professor_id=professor_id)
    if professor is None:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor
