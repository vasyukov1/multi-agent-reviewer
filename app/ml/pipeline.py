from app.config.ml_config import MLConfig
from ml.inference.auditor_inference import AuditorAgent
from ml.inference.quality_inference import QualityAgent
from ml.inference.judge_inference import JudgeAgent


class MLPipeline:
    def __init__(self, config: MLConfig):
        self.auditor = AuditorAgent(
            model_path=config.auditor_model_path,
            encoder_name=config.auditor_encoder,
        )

        self.quality = QualityAgent(
            model_path=config.quality_model_path,
            encoder_name=config.quality_encoder,
        )

        self.judge = JudgeAgent(
            model_path=config.judge_model_path,
            input_dim=config.judge_input_dim,
        )

    def process(self, text: str, meta: dict | None = None) -> dict:
        auditor_out = self.auditor.audit(text)
        quality_out = self.quality.score(text)
        
        meta = meta or {}

        verdict = self.judge.decide(
            auditor_out=auditor_out,
            quality_out=quality_out,
            meta=meta,
        )

        return {
            "verdict": verdict["verdict"],
            "confidence": verdict["confidence"],
            "scores": verdict["scores"],
            "auditor": auditor_out,
            "quality": quality_out,
        }
