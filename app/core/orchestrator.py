from app.models.schemas import AdInput, AgentIssue, ReviewResult
from app.config.ml_config import MLConfig
from app.ml.pipeline import MLPipeline


class ReviewOrchestrator:
    """
    Orchestrates multi-agent review pipeline.
    Docstring for ReviewOrchestrator
    """

    def __init__(self):
        self.ml_pipeline = MLPipeline(MLConfig())

    def run_review(self, ad: AdInput) -> dict:
        text = ad.description
        meta = {"text_length": len(text)}

        ml = self.ml_pipeline.process(text, meta=meta)

        issues = []
        for label, prob in ml["auditor"]["risk_labels"].items():
            if prob > 0.05:
                issues.append(
                    AgentIssue(
                        agent="auditor",
                        code=label,
                        message=f"Detected {label} risk: {float(prob):.4f}",
                    )
                )
        
        for k, v in ml["quality"]["aspects"].items():
            if v < 0.05:
                issues.append(
                    AgentIssue(
                        agent="quality",
                        code=k,
                        message=f"Low {k}: {float(1 - v):.4f}",
                    )
                )

        return ReviewResult(
            risk_score=ml["auditor"]["risk_score"],
            quality_score=ml["quality"]["quality_score"],
            issues=issues,
            verdict=ml["verdict"],
            improved_text=None
        )
       