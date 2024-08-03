import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db import models, database, schemas, crud
from app.utils.auth import get_current_user, authenticate_user, create_access_token

# Initialize the logger
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Log requests
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

# Route for obtaining a token
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Include other routers
from app.routers import students, books, borrows, colleges, courses, depts, educational_employees, employees, grades, professors, rooms, sections, takes

app.include_router(students.router, prefix="/api/v1")
app.include_router(books.router, prefix="/api/v1")
app.include_router(borrows.router, prefix="/api/v1")
app.include_router(colleges.router, prefix="/api/v1")
app.include_router(courses.router, prefix="/api/v1")
app.include_router(depts.router, prefix="/api/v1")
app.include_router(educational_employees.router, prefix="/api/v1")
app.include_router(employees.router, prefix="/api/v1")
app.include_router(grades.router, prefix="/api/v1")
app.include_router(professors.router, prefix="/api/v1")
app.include_router(rooms.router, prefix="/api/v1")
app.include_router(sections.router, prefix="/api/v1")
app.include_router(takes.router, prefix="/api/v1")
