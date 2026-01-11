from dataclasses import dataclass
from ml.datasets.synthetic_judge import generate_judge_sample

@dataclass(frozen=True)
class MLConfig:
    auditor_model_path: str = "weights/auditor.pt"
    quality_model_path: str = "weights/quality.pt"
    judge_model_path: str = "weights/judge.pt"

    auditor_encoder: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    quality_encoder: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    x, _ = generate_judge_sample()
    judge_input_dim: int = len(x)
