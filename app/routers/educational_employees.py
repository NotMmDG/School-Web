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

# API route to get all educational employees
@router.get("/educational_employees/", response_model=List[schemas.EducationalEmployeeOut])
def read_educational_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    educational_employees = crud.get_educational_employees(db, skip=skip, limit=limit)
    return educational_employees

# API route to get an educational employee by ID
@router.get("/educational_employees/{edu_id}", response_model=schemas.EducationalEmployeeOut)
def read_educational_employee(edu_id: int, db: Session = Depends(get_db)):
    educational_employee = crud.get_educational_employee(db, edu_id=edu_id)
    if educational_employee is None:
        raise HTTPException(status_code=404, detail="Educational employee not found")
    return educational_employee

# API route to create a new educational employee
@router.post("/educational_employees/", response_model=schemas.EducationalEmployeeOut)
def create_educational_employee(educational_employee: schemas.EducationalEmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_educational_employee(db=db, educational_employee=educational_employee)

# API route to update an educational employee by ID
@router.put("/educational_employees/{edu_id}", response_model=schemas.EducationalEmployeeOut)
def update_educational_employee(edu_id: int, educational_employee_update: schemas.EducationalEmployeeUpdate, db: Session = Depends(get_db)):
    educational_employee = crud.update_educational_employee(db=db, edu_id=edu_id, educational_employee_update=educational_employee_update)
    if educational_employee is None:
        raise HTTPException(status_code=404, detail="Educational employee not found")
    return educational_employee

# API route to delete an educational employee by ID
@router.delete("/educational_employees/{edu_id}", response_model=schemas.EducationalEmployeeOut)
def delete_educational_employee(edu_id: int, db: Session = Depends(get_db)):
    educational_employee = crud.delete_educational_employee(db=db, edu_id=edu_id)
    if educational_employee is None:
        raise HTTPException(status_code=404, detail="Educational employee not found")
    return educational_employee
