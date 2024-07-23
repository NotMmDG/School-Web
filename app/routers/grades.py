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

# API route to get all grades
@router.get("/grades/", response_model=List[models.Grade])
def read_grades(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    grades = crud.get_grades(db, skip=skip, limit=limit)
    return grades

# API route to get a grade by ID
@router.get("/grades/{grade_id}", response_model=models.Grade)
def read_grade(grade_id: int, db: Session = Depends(get_db)):
    grade = crud.get_grade(db, grade_id=grade_id)
    if grade is None:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade

# API route to create a new grade
@router.post("/grades/", response_model=models.Grade)
def create_grade(grade: models.Grade, db: Session = Depends(get_db)):
    return crud.create_grade(db=db, grade=grade)

# API route to update a grade by ID
@router.put("/grades/{grade_id}", response_model=models.Grade)
def update_grade(grade_id: int, grade_value: int, db: Session = Depends(get_db)):
    grade = crud.update_grade(db=db, grade_id=grade_id, grade_value=grade_value)
    if grade is None:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade

# API route to delete a grade by ID
@router.delete("/grades/{grade_id}", response_model=models.Grade)
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    grade = crud.delete_grade(db=db, grade_id=grade_id)
    if grade is None:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade
