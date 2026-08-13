from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventCreate


def create_event(db: Session, event: EventCreate):
    new_event = Event(
        truck_id=event.truck_id,
        temperature=event.temperature,
        humidity=event.humidity,
        speed=event.speed,
        gps_location=event.gps_location,
        fuel_level=event.fuel_level,
        timestamp=event.timestamp,
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


def get_events(db: Session):
    return db.query(Event).all()

from sqlalchemy import func


def get_statistics(db: Session):
    total = db.query(Event).count()

    avg_temp = db.query(func.avg(Event.temperature)).scalar()
    max_temp = db.query(func.max(Event.temperature)).scalar()
    min_temp = db.query(func.min(Event.temperature)).scalar()

    return {
        "total_events": total,
        "average_temperature": round(avg_temp, 2) if avg_temp else 0,
        "highest_temperature": max_temp,
        "lowest_temperature": min_temp
    }

def get_alerts(db: Session):
    alerts = db.query(Event).filter(Event.temperature > 35).all()
    return alerts

def get_workers():
    return [
        {
            "worker_id": 1,
            "status": "Running",
            "processed_events": 1200
        },
        {
            "worker_id": 2,
            "status": "Running",
            "processed_events": 1150
        },
        {
            "worker_id": 3,
            "status": "Idle",
            "processed_events": 980
        }
    ]

def get_workers():
    return [
        {
            "worker_id": 1,
            "status": "Running",
            "processed_events": 1200
        },
        {
            "worker_id": 2,
            "status": "Running",
            "processed_events": 1150
        },
        {
            "worker_id": 3,
            "status": "Idle",
            "processed_events": 980
        }
    ]
worker_heartbeats = {}


def update_worker_heartbeat(worker_id: str):
    worker_heartbeats[worker_id] = {
        "worker_id": worker_id,
        "status": "Running"
    }
    return worker_heartbeats[worker_id]


def get_worker_heartbeats():
    return list(worker_heartbeats.values())