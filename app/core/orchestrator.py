from typing import List, Optional

from app.models.schemas import AdInput, AgentIssue, ReviewResult
from app.config.ml_config import MLConfig
from app.ml.pipeline import MLPipeline
from app.agents.cv_inspector import analyze_images


class ReviewOrchestrator:
    """
    Orchestrates multi-agent review pipeline.
    Docstring for ReviewOrchestrator
    """

    def __init__(self):
        self.ml_pipeline = MLPipeline(MLConfig())

    def run_review(
        self,
        ad: AdInput,
        images: Optional[List[bytes]] = None,
    ) -> ReviewResult:
        text = ad.description
        meta = {"text_length": len(text)}

        # ---- TEXT ML PIPELINE ----
        ml = self.ml_pipeline.process(text, meta=meta)

        issues: list[AgentIssue] = []

        for label, prob in ml["auditor"]["risk_labels"].items():
            # if prob > 0.05:
            issues.append(
                AgentIssue(
                    agent="auditor",
                    code=label,
                    message=f"Detected {label} risk: {float(prob):.4f}",
                )
            )
        
        for k, v in ml["quality"]["aspects"].items():
            # if v < 0.05:
            issues.append(
                AgentIssue(
                    agent="quality",
                    code=k,
                    message=f"Low {k}: {float(1 - v):.4f}",
                )
            )
        
        text_quality_score = ml["quality"]["quality_score"]

        # ---- CV INSPECTOR ----
        cv_score = None
        if images:
            cv_result = analyze_images(images, ad_text=text)
            cv_score = cv_result.cv_score

            issues.extend(cv_result.image_issues)
        else:
            cv_result = None

        # ---- AGGREGATION ----
        # Quality = 70% Text + 30% CV
        if cv_score is not None:
            final_quality_score = 0.7 * text_quality_score + 0.3 * cv_score
        else:
            final_quality_score = text_quality_score

        return ReviewResult(
            risk_score=ml["auditor"]["risk_score"],
            quality_score=final_quality_score,
            issues=issues,
            verdict=ml["verdict"],
            improved_text=None,
        )
       