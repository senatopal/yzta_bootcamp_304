from pydantic import BaseModel

class HouseholdBase(BaseModel):
    LCLid: str
    stdorToU: str
    acorn_grouped: str

class HouseholdCreate(HouseholdBase):
    pass

class HouseholdResponse(HouseholdBase):
    
    class Config:
        from_attributes = True  # Required for ORM model mapping in Pydantic v2
