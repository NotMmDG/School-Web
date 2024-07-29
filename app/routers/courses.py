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

# API route to get all courses
@router.get("/courses/", response_model=List[schemas.CourseOut])
def read_courses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    courses = crud.get_courses(db, skip=skip, limit=limit)
    return courses

# API route to get a course by ID
@router.get("/courses/{course_code}", response_model=schemas.CourseOut)
def read_course(course_code: int, db: Session = Depends(get_db)):
    course = crud.get_course(db, course_code=course_code)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# API route to create a new course
@router.post("/courses/", response_model=schemas.CourseOut)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db=db, course=course)

# API route to update a course by ID
@router.put("/courses/{course_code}", response_model=schemas.CourseOut)
def update_course(course_code: int, course_update: schemas.CourseUpdate, db: Session = Depends(get_db)):
    course = crud.update_course(db=db, course_code=course_code, course_update=course_update)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# API route to delete a course by ID
@router.delete("/courses/{course_code}", response_model=schemas.CourseOut)
def delete_course(course_code: int, db: Session = Depends(get_db)):
    course = crud.delete_course(db=db, course_code=course_code)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# Get available courses for the next semester
@router.get("/available_courses/", response_model=List[schemas.SectionOut])
def read_available_courses(semester: str, year: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    courses = crud.get_available_courses(db, semester=semester, year=year, skip=skip, limit=limit)
    return courses

# Register course selection for a student
@router.post("/register_course/")
def register_course(student_id: int, section_id: int, db: Session = Depends(get_db)):
    section = crud.register_course_selection(db, student_id=student_id, section_id=section_id)
    if section is None:
        raise HTTPException(status_code=404, detail="Section or Student not found")
    return {"message": "Course registered successfully"}
