from fastapi import APIRouter
from app.models.schemas import AdInput, ReviewResult
from app.core.orchestrator import ReviewOrchestrator
from app.services.persistence import ReviewPersistence

router = APIRouter(prefix="/api")

orchestrator = ReviewOrchestrator()
persistence = ReviewPersistence()


@router.post("/review", response_model=ReviewResult)
def review_ad(ad: AdInput) -> ReviewResult:
    """
    Docstring for review_ad
    
    :param ad: Description
    :type ad: AdInput
    :return: Description
    :rtype: ReviewResult
    """
    result = orchestrator.run_review(ad)
    persistence.save(ad=ad, result=result)
    
    return result
