from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.event import EventCreate, EventResponse
from app.services.event_service import (
    create_event,
    get_events,
    get_statistics,
    get_alerts,
    get_worker_heartbeats,
    get_workers,
    update_worker_heartbeat,
    get_worker_heartbeats
)
router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


# POST - Create Event
@router.post("/", response_model=EventResponse)
def add_event(event: EventCreate, db: Session = Depends(get_db)):
    return create_event(db, event)


# GET - All Events
@router.get("/", response_model=list[EventResponse])
def read_events(db: Session = Depends(get_db)):
    return get_events(db)


# GET - Statistics
@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    return get_statistics(db)


# GET - Alerts (Temperature > 35°C)
@router.get("/alerts", response_model=list[EventResponse])
def alerts(db: Session = Depends(get_db)):
    return get_alerts(db)


# GET - Workers
@router.get("/workers")
def workers():
    return get_workers()
# POST - Worker Heartbeat
@router.post("/workers/heartbeat")
def worker_heartbeat(worker_id: str):
    return update_worker_heartbeat(worker_id)


# GET - Live Worker Heartbeats
@router.get("/workers/heartbeat")
def worker_heartbeat_status():
    return get_worker_heartbeats()