from fastapi import FastAPI
from database import engine, Base

from models.user import User

from models.application import (
    Application,
    Note,
    StatusLog
)

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "DevTrack API Running"}