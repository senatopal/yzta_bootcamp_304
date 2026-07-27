from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.household import Household
from app.schemas.coach import CoachContextResponse
from app.services.coach import CoachService

from fastapi import HTTPException

from app.schemas.coach import (
    CoachChatRequest,
    CoachChatResponse,
)
from app.services.llm import (
    LLMConfigurationError,
    LLMRateLimitError,
    LLMService,
    LLMServiceError,
)

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


@router.post(
    "/coach/chat",
    response_model=CoachChatResponse,
)
def chat_with_coach(
    request: CoachChatRequest,
    db: Session = Depends(get_db),
) -> CoachChatResponse:
    context = CoachService.get_grounding_context(
        db,
        request.household_id,
    )

    try:
        result = LLMService.generate_answer(
            user_message=request.message,
            prompt_context=context.get("prompt_context", ""),
            history=[
                message.model_dump()
                for message in request.history
            ],
        )

    except LLMConfigurationError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    except LLMRateLimitError as exc:
        raise HTTPException(
            status_code=429,
            detail=str(exc),
        ) from exc

    except LLMServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    return CoachChatResponse(
        household_id=request.household_id,
        answer=str(result["answer"]),
        model=str(result["model"]),
        response_id=result.get("response_id"),
        grounded=True,
    )