from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional

from app.models.schemas import AdInput, ReviewResult
from app.core.orchestrator import ReviewOrchestrator
from app.services.persistence import ReviewPersistence

router = APIRouter(prefix="/api")

orchestrator = ReviewOrchestrator()
persistence = ReviewPersistence()


@router.post("/review", response_model=ReviewResult)
async def review_ad(
    title: str = Form(...),
    description: str = Form(...),
    category: Optional[str] = Form(None),
    images: Optional[List[UploadFile]] = File(None),
) -> ReviewResult:
    """
    Docstring for review_ad
    
    :param title: Description
    :type title: str
    :param description: Description
    :type description: str
    :param category: Description
    :type category: Optional[str]
    :param images: Description
    :type images: Optional[List[UploadFile]]
    :return: Description
    :rtype: ReviewResult
    """
    ad = AdInput(
        title=title,
        description=description,
        category=category,
    )

    image_bytes = []
    if images:
        for img in images:
            image_bytes.append(await img.read())

    result = orchestrator.run_review(ad, images=image_bytes)
    persistence.save(ad=ad, result=result)
    
    return result
