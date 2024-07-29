from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import crud, models, database, schemas

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API route to get all takes
@router.get("/takes/", response_model=List[schemas.TakesOut])
def read_takes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    takes = crud.get_takes(db, skip=skip, limit=limit)
    return takes

# API route to get a take by ID
@router.get("/takes/{take_id}", response_model=schemas.TakesOut)
def read_take(take_id: int, db: Session = Depends(get_db)):
    take = crud.get_take(db, take_id=take_id)
    if take is None:
        raise HTTPException(status_code=404, detail="Take not found")
    return take

# API route to create a new take
@router.post("/takes/", response_model=schemas.TakesOut)
def create_take(take: schemas.TakesCreate, db: Session = Depends(get_db)):
    return crud.create_take(db=db, take=take)

# API route to update a take by ID
@router.put("/takes/{take_id}", response_model=schemas.TakesOut)
def update_take(take_id: int, take_update: schemas.TakesUpdate, db: Session = Depends(get_db)):
    take = crud.update_take(db=db, take_id=take_id, take_update=take_update)
    if take is None:
        raise HTTPException(status_code=404, detail="Take not found")
    return take

# API route to delete a take by ID
@router.delete("/takes/{take_id}", response_model=schemas.TakesOut)
def delete_take(take_id: int, db: Session = Depends(get_db)):
    take = crud.delete_take(db=db, take_id=take_id)
    if take is None:
        raise HTTPException(status_code=404, detail="Take not found")
    return take
