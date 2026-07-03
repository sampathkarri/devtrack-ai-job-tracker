from fastapi import FastAPI

from database import engine, Base

from models.user import User

from models.application import (
    Application,
    Note,
    StatusLog
)

from routers.auth import router as auth_router
from routers.application import router as application_router
from routers.dashboard import router as dashboard_router

from routers.ai import router as ai_router
app = FastAPI()

app.include_router(auth_router)
app.include_router(application_router)
app.include_router(dashboard_router)
app.include_router(ai_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "DevTrack API Running"}