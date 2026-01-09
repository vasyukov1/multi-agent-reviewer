from fastapi import APIRouter
from app.models.schemas import AdInput, ReviewResult, AgentIssue

router = APIRouter(prefix="/api")

@router.post("/review", response_model=ReviewResult)
def review_ad(ad: AdInput) -> ReviewResult:
    """
    Docstring for review_ad
    
    :param ad: Description
    :type ad: AdInput
    :return: Description
    :rtype: ReviewResult
    """
    # Заглушка оркестратора - будет заменена на real orchestrator
    return ReviewResult(
        risk_score=0.0,
        quality_score=0.5,
        verdict="revise",
        improved_text=None,
        issue=[
            AgentIssue(
                agent="stub",
                code="NOT_IMPLEMENTED",
                message="Review logic is not implemented yet",
            )
        ],
    )