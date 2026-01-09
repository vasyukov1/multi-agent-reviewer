from fastapi import APIRouter
from app.models.schemas import AdInput, ReviewResult, AgentIssue
from app.core.orchestrator import ReviewOrchestrator

router = APIRouter(prefix="/api")

orchestrator = ReviewOrchestrator()


@router.post("/review", response_model=ReviewResult)
def review_ad(ad: AdInput) -> ReviewResult:
    """
    Docstring for review_ad
    
    :param ad: Description
    :type ad: AdInput
    :return: Description
    :rtype: ReviewResult
    """
    return orchestrator.run_review(ad)