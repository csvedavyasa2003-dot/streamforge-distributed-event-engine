from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import Base, engine
from app.models.event import Event
from app.routers.event_router import router as event_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="StreamForge Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(event_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to StreamForge Backend"
    }