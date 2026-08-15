from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.event import Event
import time
import uuid


from app.database.connection import get_db
from app.schemas.event import EventCreate, EventResponse
from rocksdict import Rdict, AccessType
from app.services.event_service import (
    create_event,
    get_events,
    get_statistics,
    get_alerts,
    get_workers
)
router = APIRouter(
    prefix="/events",
    tags=["Events"]
)
# In-memory heartbeat store: { worker_id: last_seen_timestamp }
worker_heartbeats = {}
HEARTBEAT_TIMEOUT_SECONDS = 15  # if no heartbeat in this window, consider worker "down"

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

# DELETE - Reset all events (for demo/testing purposes)
@router.delete("/reset")
def reset_events(db: Session = Depends(get_db)):
    db.query(Event).delete()
    db.commit()
    return {"status": "All events cleared"}

# GET - Live Windows (in-progress windowed aggregation state)
@router.get("/live-windows")
def live_windows():
    try:
        db = Rdict("rocksdb_state", access_type=AccessType.read_only())
    except Exception as e:
        return {"error": f"Could not read live window state: {e}"}

    result = []
    for key in db.keys():
        truck_id, window_start = key.split(":")
        temps = db[key]
        avg = sum(temps) / len(temps) if temps else 0
        result.append({
            "truck_id": truck_id,
            "window_start": int(window_start),
            "event_count": len(temps),
            "current_avg_temp": round(avg, 2),
        })

        

    db.close()
    return result

# POST - Worker Heartbeat
@router.post("/workers/heartbeat")
def worker_heartbeat(worker_id: str):
    worker_heartbeats[worker_id] = time.time()
    return {"status": "ok", "worker_id": worker_id}


# GET - Real Worker Status (derived from heartbeats)
@router.get("/workers/live")
def live_workers():
    now = time.time()
    result = []
    for worker_id, last_seen in worker_heartbeats.items():
        age = now - last_seen
        status = "Running" if age <= HEARTBEAT_TIMEOUT_SECONDS else "Down"
        result.append({
            "worker_id": worker_id,
            "status": status,
            "last_seen_seconds_ago": round(age, 1),
        })
    return result




