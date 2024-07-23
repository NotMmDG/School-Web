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

# API route to get all employees
@router.get("/employees/", response_model=List[models.Employee])
def read_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees

# API route to get an employee by ID
@router.get("/employees/{employee_id}", response_model=models.Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = crud.get_employee(db, employee_id=employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# API route to create a new employee
@router.post("/employees/", response_model=models.Employee)
def create_employee(employee: models.Employee, db: Session = Depends(get_db)):
    return crud.create_employee(db=db, employee=employee)

# API route to update an employee by ID
@router.put("/employees/{employee_id}", response_model=models.Employee)
def update_employee(employee_id: int, first_name: str = None, last_name: str = None, position: str = None, salary: int = None, department_id: int = None, db: Session = Depends(get_db)):
    employee = crud.update_employee(db=db, employee_id=employee_id, first_name=first_name, last_name=last_name, position=position, salary=salary, department_id=department_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# API route to delete an employee by ID
@router.delete("/employees/{employee_id}", response_model=models.Employee)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = crud.delete_employee(db=db, employee_id=employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
