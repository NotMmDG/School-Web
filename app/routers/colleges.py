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

# API route to get all colleges
@router.get("/colleges/", response_model=List[models.College])
def read_colleges(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    colleges = crud.get_colleges(db, skip=skip, limit=limit)
    return colleges

# API route to get a college by ID
@router.get("/colleges/{college_id}", response_model=models.College)
def read_college(college_id: int, db: Session = Depends(get_db)):
    college = crud.get_college(db, college_id=college_id)
    if college is None:
        raise HTTPException(status_code=404, detail="College not found")
    return college

# API route to create a new college
@router.post("/colleges/", response_model=models.College)
def create_college(college: models.College, db: Session = Depends(get_db)):
    return crud.create_college(db=db, college=college)

# API route to update a college by ID
@router.put("/colleges/{college_id}", response_model=models.College)
def update_college(college_id: int, name: str = None, office: int = None, phone: str = None, dean: int = None, apikey: str = None, db: Session = Depends(get_db)):
    college = crud.update_college(db=db, college_id=college_id, name=name, office=office, phone=phone, dean=dean, apikey=apikey)
    if college is None:
        raise HTTPException(status_code=404, detail="College not found")
    return college

# API route to delete a college by ID
@router.delete("/colleges/{college_id}", response_model=models.College)
def delete_college(college_id: int, db: Session = Depends(get_db)):
    college = crud.delete_college(db=db, college_id=college_id)
    if college is None:
        raise HTTPException(status_code=404, detail="College not found")
    return college
