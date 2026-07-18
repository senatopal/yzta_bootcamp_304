from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.household import Household
from app.schemas.household import HouseholdResponse

router = APIRouter()

@router.get("/households", response_model=List[HouseholdResponse], tags=["Households"])
def list_households(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get list of registered households with pagination.
    """
    households = db.query(Household).offset(skip).limit(limit).all()
    return households

@router.get("/households/{lclid}", response_model=HouseholdResponse, tags=["Households"])
def get_household(lclid: str, db: Session = Depends(get_db)):
    """
    Get detailed profile of a specific household.
    """
    household = db.query(Household).filter(Household.LCLid == lclid).first()
    if not household:
        raise HTTPException(status_code=404, detail=f"Household {lclid} not found")
    return household
