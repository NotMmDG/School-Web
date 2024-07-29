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

# API route to get all rooms
@router.get("/rooms/", response_model=List[schemas.RoomOut])
def read_rooms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    rooms = crud.get_rooms(db, skip=skip, limit=limit)
    return rooms

# API route to get a room by code
@router.get("/rooms/{room_code}", response_model=schemas.RoomOut)
def read_room(room_code: int, db: Session = Depends(get_db)):
    room = crud.get_room(db, room_code=room_code)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

# API route to create a new room
@router.post("/rooms/", response_model=schemas.RoomOut)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_room(db=db, room=room)

# API route to update a room by code
@router.put("/rooms/{room_code}", response_model=schemas.RoomOut)
def update_room(room_code: int, room_update: schemas.RoomUpdate, db: Session = Depends(get_db)):
    room = crud.update_room(db=db, room_code=room_code, room_update=room_update)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

# API route to delete a room by code
@router.delete("/rooms/{room_code}", response_model=schemas.RoomOut)
def delete_room(room_code: int, db: Session = Depends(get_db)):
    room = crud.delete_room(db=db, room_code=room_code)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return room
