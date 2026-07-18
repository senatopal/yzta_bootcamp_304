from sqlalchemy import Column, String
from app.core.database import Base

class Household(Base):
    __tablename__ = "households"
    
    LCLid = Column(String(15), primary_key=True, index=True)
    stdorToU = Column(String(10), nullable=False)
    acorn_grouped = Column(String(30), nullable=False)
