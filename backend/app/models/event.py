from sqlalchemy import Column, Integer, Float, String
from app.database.connection import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    truck_id = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    speed = Column(Float)
    gps_location = Column(String)
    fuel_level = Column(Float)
    timestamp = Column(String)