import torch
from transformers import AutoTokenizer
from ml.models.quality_model import QualityModel


class QualityAgent:
    def __init__(self, model_path: str, encoder_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(encoder_name)
        self.model = QualityModel(encoder_name)
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    @torch.no_grad()
    def score(self, text: str):
        tokens = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
        )

        out = self.model(**tokens)
        aspects = {k: float(v.item()) for k, v in out["aspects"].items()}

        return {
            "quality_score": float(out["quality_score"].item()),
            "aspects": aspects,
            "confidence": 1 - torch.std(torch.tensor(list(aspects.values()))).item(),
        }
