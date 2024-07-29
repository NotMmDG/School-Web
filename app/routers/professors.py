from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import crud, schemas, database

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API route to get all professors
@router.get("/professors/", response_model=List[schemas.ProfessorOut])
def read_professors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    professors = crud.get_professors(db, skip=skip, limit=limit)
    return professors

# API route to get a professor by ID
@router.get("/professors/{professor_id}", response_model=schemas.ProfessorOut)
def read_professor(professor_id: int, db: Session = Depends(get_db)):
    professor = crud.get_professor(db, professor_id=professor_id)
    if professor is None:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor

# API route to create a new professor
@router.post("/professors/", response_model=schemas.ProfessorOut)
def create_professor(professor: schemas.ProfessorCreate, db: Session = Depends(get_db)):
    return crud.create_professor(db=db, professor=professor)

# API route to update a professor by ID
@router.put("/professors/{professor_id}", response_model=schemas.ProfessorOut)
def update_professor(professor_id: int, professor_update: schemas.ProfessorUpdate, db: Session = Depends(get_db)):
    professor = crud.update_professor(db=db, professor_id=professor_id, professor_update=professor_update)
    if professor is None:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor

# API route to delete a professor by ID
@router.delete("/professors/{professor_id}", response_model=schemas.ProfessorOut)
def delete_professor(professor_id: int, db: Session = Depends(get_db)):
    professor = crud.delete_professor(db=db, professor_id=professor_id)
    if professor is None:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor
