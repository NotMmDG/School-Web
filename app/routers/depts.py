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

# API route to get all departments
@router.get("/depts/", response_model=List[models.Dept])
def read_depts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    depts = crud.get_depts(db, skip=skip, limit=limit)
    return depts

# API route to get a department by code
@router.get("/depts/{dept_code}", response_model=models.Dept)
def read_dept(dept_code: int, db: Session = Depends(get_db)):
    dept = crud.get_dept(db, dept_code=dept_code)
    if dept is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

# API route to create a new department
@router.post("/depts/", response_model=models.Dept)
def create_dept(dept: models.Dept, db: Session = Depends(get_db)):
    return crud.create_dept(db=db, dept=dept)

# API route to update a department by code
@router.put("/depts/{dept_code}", response_model=models.Dept)
def update_dept(dept_code: int, name: str = None, office: int = None, phone: str = None, college_id: int = None, db: Session = Depends(get_db)):
    dept = crud.update_dept(db=db, dept_code=dept_code, name=name, office=office, phone=phone, college_id=college_id)
    if dept is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

# API route to delete a department by code
@router.delete("/depts/{dept_code}", response_model=models.Dept)
def delete_dept(dept_code: int, db: Session = Depends(get_db)):
    dept = crud.delete_dept(db=db, dept_code=dept_code)
    if dept is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept
