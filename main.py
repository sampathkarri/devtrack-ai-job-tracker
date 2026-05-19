from fastapi import FastAPI
from database import engine, Base

from models.user import User

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "DevTrack API Running"}