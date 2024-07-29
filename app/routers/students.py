from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import crud, models, database, schemas
from app.utils.auth import get_current_user

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API route to get all students
@router.get("/students/", response_model=List[schemas.StudentOut])
def read_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

# API route to get a student by ID
@router.get("/students/{student_id}", response_model=schemas.StudentOut)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# API route to create a new student
@router.post("/students/", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db=db, student=student)

# API route to update a student by ID
@router.put("/students/{student_id}", response_model=schemas.StudentOut)
def update_student(student_id: int, student_update: schemas.StudentUpdate, db: Session = Depends(get_db)):
    student = crud.update_student(db=db, student_id=student_id, student_update=student_update)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# API route to delete a student by ID
@router.delete("/students/{student_id}", response_model=schemas.StudentOut)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.delete_student(db=db, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/grades/{student_id}/{semester}/{year}", response_model=List[schemas.GradeOut])
def read_grades(student_id: int, semester: str, year: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    grades = crud.get_grades_by_student_and_semester(db, student_id=student_id, semester=semester, year=year)
    if not grades:
        raise HTTPException(status_code=404, detail="Grades not found")
    return grades
