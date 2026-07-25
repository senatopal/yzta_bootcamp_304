from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.household import Household
from app.schemas.coach import CoachContextResponse
from app.services.coach import CoachService

router = APIRouter()

@router.get(
    "/coach/context",
    response_model=CoachContextResponse,
    tags=["Coach"]
)
def get_coach_context(
    household_id: str = Query(..., description="LCLid of the household"),
    db: Session = Depends(get_db)
):
    """
    Retrieves aggregated weekly consumption, savings recommendations, and anomalies for a household
    packaged into structured JSON and a pre-formatted prompt context string for LLM grounding.
    """
    # Verify if the household exists first
    household = db.query(Household).filter(Household.LCLid == household_id).first()
    if not household:
        raise HTTPException(status_code=404, detail=f"Household {household_id} not found")

    return CoachService.get_grounding_context(db, household_id)
