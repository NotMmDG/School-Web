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

# API route to get all sections
@router.get("/sections/", response_model=List[schemas.SectionOut])
def read_sections(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    sections = crud.get_sections(db, skip=skip, limit=limit)
    return sections

# API route to get a section by ID
@router.get("/sections/{section_id}", response_model=schemas.SectionOut)
def read_section(section_id: int, db: Session = Depends(get_db)):
    section = crud.get_section(db, section_id=section_id)
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    return section

# API route to create a new section
@router.post("/sections/", response_model=schemas.SectionOut)
def create_section(section: schemas.SectionCreate, db: Session = Depends(get_db)):
    return crud.create_section(db=db, section=section)

# API route to update a section by ID
@router.put("/sections/{section_id}", response_model=schemas.SectionOut)
def update_section(section_id: int, section_update: schemas.SectionUpdate, db: Session = Depends(get_db)):
    section = crud.update_section(db=db, section_id=section_id, section_update=section_update)
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    return section

# API route to delete a section by ID
@router.delete("/sections/{section_id}", response_model=schemas.SectionOut)
def delete_section(section_id: int, db: Session = Depends(get_db)):
    section = crud.delete_section(db=db, section_id=section_id)
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    return section
