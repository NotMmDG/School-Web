from .database import SessionLocal, engine
from . import models

# Create all tables in the database. This is to be used for the initial setup.
def init_db():
    models.Base.metadata.create_all(bind=engine)

__all__ = ["init_db", "SessionLocal", "engine"]
