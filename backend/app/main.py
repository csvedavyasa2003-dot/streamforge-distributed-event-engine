from fastapi import FastAPI
from app.database.connection import Base, engine
from app.models.event import Event
from app.routers.event_router import router as event_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="StreamForge Backend")

app.include_router(event_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to StreamForge Backend"
    }