from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.event import Event
from app.database.connection import get_db
from app.schemas.event import EventCreate, EventResponse

from app.services.event_service import (
    create_event,
    get_events,
    get_statistics,
    get_alerts,
    get_workers,
)

from rocksdict import Rdict, AccessType
import time


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


# ============================================================
# Worker Heartbeat Storage
# ============================================================

worker_heartbeats = {}

HEARTBEAT_TIMEOUT_SECONDS = 15


# ============================================================
# POST - Create Event
# ============================================================

@router.post("/", response_model=EventResponse)
def add_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):
    return create_event(db, event)


# ============================================================
# GET - All Events
# ============================================================

@router.get("/", response_model=list[EventResponse])
def read_events(
    db: Session = Depends(get_db)
):
    return get_events(db)


# ============================================================
# GET - Statistics
# ============================================================

@router.get("/stats")
def stats(
    db: Session = Depends(get_db)
):
    return get_statistics(db)


# ============================================================
# GET - Alerts
# ============================================================

@router.get(
    "/alerts",
    response_model=list[EventResponse]
)
def alerts(
    db: Session = Depends(get_db)
):
    return get_alerts(db)


# ============================================================
# GET - Workers
# ============================================================

@router.get("/workers")
def workers():
    return get_workers()


# ============================================================
# POST - Worker Heartbeat
# ============================================================

@router.post("/workers/heartbeat")
def worker_heartbeat(worker_id: str):

    worker_heartbeats[worker_id] = time.time()

    return {
        "status": "ok",
        "worker_id": worker_id
    }


# ============================================================
# GET - Worker Heartbeat Status
# ============================================================

@router.get("/workers/heartbeat")
def worker_heartbeat_status():

    now = time.time()

    result = []

    for worker_id, last_seen in worker_heartbeats.items():

        result.append({
            "worker_id": worker_id,
            "last_seen_seconds_ago": round(
                now - last_seen,
                1
            )
        })

    return result


# ============================================================
# GET - Live Workers
# ============================================================

@router.get("/workers/live")
def live_workers():

    now = time.time()

    result = []

    for worker_id, last_seen in worker_heartbeats.items():

        age = now - last_seen

        status = (
            "Running"
            if age <= HEARTBEAT_TIMEOUT_SECONDS
            else "Down"
        )

        result.append({
            "worker_id": worker_id,
            "status": status,
            "last_seen_seconds_ago": round(
                age,
                1
            )
        })

    return result


# ============================================================
# GET - Live RocksDB Windows
# ============================================================

@router.get("/live-windows")
def live_windows():

    try:

        db = Rdict(
            "rocksdb_state",
            access_type=AccessType.read_only()
        )

    except Exception as e:

        return {
            "error": f"Could not read live window state: {e}"
        }

    result = []

    for key in db.keys():

        key = str(key)

        try:

            truck_id, window_start = key.split(":", 1)

            temps = db[key]

            avg_temp = (
                sum(temps) / len(temps)
                if temps
                else 0
            )

            result.append({
                "truck_id": truck_id,
                "window_start": int(window_start),
                "event_count": len(temps),
                "current_avg_temp": round(
                    avg_temp,
                    2
                )
            })

        except Exception:

            continue

    db.close()

    return result