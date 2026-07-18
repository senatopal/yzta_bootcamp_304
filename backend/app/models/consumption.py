from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from app.core.database import Base

class ConsumptionReading(Base):
    __tablename__ = "consumption_readings"
    
    tstp = Column(DateTime, primary_key=True)
    LCLid = Column(String(15), ForeignKey("households.LCLid"), primary_key=True)
    energy_kwh = Column(Float)
    price_pence = Column(Float)
    cost_pounds = Column(Float)
