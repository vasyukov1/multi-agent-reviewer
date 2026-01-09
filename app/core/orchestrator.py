import logging
from typing import List

from app.agents.auditor import AuditorAgent
from app.agents.quality import QualityAgent
from app.agents.judge import JudgeAgent
from app.models.schemas import AdInput, AgentIssue, ReviewResult

logger = logging.getLogger(__name__)


class ReviewOrchestrator:
    """
    Orchestrates multi-agent review pipeline.
    Docstring for ReviewOrchestrator
    """

    def __init__(self):
        self.auditor = AuditorAgent()
        self.quality = QualityAgent()
        self.judge = JudgeAgent()

    def run_review(self, ad: AdInput) -> ReviewResult:
        logger.info("Starting ad review")

        # Auditor
        risk_score, auditor_issues = self.auditor.analyze(ad)
        logger.debug(
            "Auditor result",
            extra={
                "risk_score": risk_score,
                "issues": len(auditor_issues),
            },
        )

        # Quality
        quality_score, quality_issues = self.quality.analyze(ad)
        logger.debug(
            "Quality result",
            extra={
                "quality_score": quality_score,
                "issues": len(quality_issues),
            },
        )

        # Aggregate issues
        all_issues: List[AgentIssue] = auditor_issues + quality_issues

        # Judge
        final_score, verdict, final_issues = self.judge.aggregate(
            risk_score=risk_score,
            quality_score=quality_score,
            issues=all_issues,
        )

        logger.info(
            "Review completed",
            extra={
                "final_score": final_score,
                "verdict": verdict,
                "risk_score": risk_score,
                "quality_score": quality_score,
            },
        )

        return ReviewResult(
            risk_score=risk_score,
            quality_score=quality_score,
            issue=final_issues,
            verdict=verdict,
            improved_text=None,
        )
       