from sqlalchemy import Column, String, DateTime, Float
from app.core.database import Base

class WeatherReading(Base):
    __tablename__ = "weather_readings"
    
    tstp = Column(DateTime, primary_key=True)
    visibility = Column(Float)
    wind_bearing = Column(Float)
    temperature = Column(Float)
    dew_point = Column(Float)
    pressure = Column(Float)
    apparent_temperature = Column(Float)
    wind_speed = Column(Float)
    precip_type = Column(String(25))
    icon = Column(String(35))
    humidity = Column(Float)
    summary = Column(String(65))
