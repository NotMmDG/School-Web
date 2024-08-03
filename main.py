import logging
import time
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from app.db import crud, models, database, schemas
from app.utils.auth import get_current_user, authenticate_user, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

logger = logging.getLogger("main")
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Middleware to log requests and responses
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        process_time = time.time() - start_time
        if hasattr(response, "body"):
            logger.info(f"Response: {response.status_code} {response.body}")
        else:
            logger.info(f"Response: {response.status_code} (streaming response)")
        logger.info(f"Process time: {process_time:.4f} sec")
        return response

app.add_middleware(LoggingMiddleware)

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Token endpoint
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Current user endpoint
@app.get("/users/me", response_model=schemas.UserOut)
async def read_users_me(current_user: schemas.UserOut = Depends(get_current_user)):
    return current_user
