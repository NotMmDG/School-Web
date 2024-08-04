import logging
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.db import models, database, schemas, crud
from app.utils.auth import authenticate_user, create_access_token
import os

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

# Serve static files
app.mount("/static", StaticFiles(directory="app/frontend/public"), name="static")

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Log requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
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
from app.routers import students, books, borrows, colleges, courses, depts, educational_employees

app.include_router(students.router)
app.include_router(books.router)
app.include_router(borrows.router)
app.include_router(colleges.router)
app.include_router(courses.router)
app.include_router(depts.router)
app.include_router(educational_employees.router)

# Catch-all route to serve the frontend
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    return FileResponse('app/frontend/public/index.html')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("WEB_PORT", 8000)))
