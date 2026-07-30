from pydantic import BaseModel


class EventCreate(BaseModel):
    truck_id: str
    temperature: float
    humidity: float
    speed: float
    gps_location: str
    fuel_level: float
    timestamp: str


class EventResponse(EventCreate):
    id: int

    class Config:
        from_attributes = True