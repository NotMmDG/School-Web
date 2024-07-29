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

# API route to get all employees
@router.get("/employees/", response_model=List[schemas.EmployeeOut])
def read_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees

# API route to get an employee by ID
@router.get("/employees/{employee_id}", response_model=schemas.EmployeeOut)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = crud.get_employee(db, employee_id=employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# API route to create a new employee
@router.post("/employees/", response_model=schemas.EmployeeOut)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db=db, employee=employee)

# API route to update an employee by ID
@router.put("/employees/{employee_id}", response_model=schemas.EmployeeOut)
def update_employee(employee_id: int, employee_update: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    employee = crud.update_employee(db=db, employee_id=employee_id, employee_update=employee_update)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# API route to delete an employee by ID
@router.delete("/employees/{employee_id}", response_model=schemas.EmployeeOut)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = crud.delete_employee(db=db, employee_id=employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
