import torch
import numpy as np
from ml.models.judge_model import JudgeModel
from ml.features.judge_features import build_judge_features

VERDICTS = ["publish", "revise", "reject"]


class JudgeAgent:
    def __init__(self, model_path: str, input_dim: int):
        self.model = JudgeModel(input_dim=input_dim)
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    @torch.no_grad()
    def decide(self, auditor_out, quality_out, meta=None):
        features = build_judge_features(auditor_out, quality_out, meta)
        x = torch.tensor(features).unsqueeze(0)

        out = self.model(x)
        probs = out["probs"].squeeze(0).numpy()

        idx = int(np.argmax(probs))

        return {
            "verdict": VERDICTS[idx],
            "confidence": float(probs[idx]),
            "scores": {
                VERDICTS[i]: float(probs[i]) for i in range(len(VERDICTS))
            }
        }
