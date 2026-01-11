import torch
from transformers import AutoTokenizer
from ml.models.auditor_model import AuditorModel, RISK_LABELS


class AuditorAgent:
    def __init__(self, model_path: str, encoder_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(encoder_name)
        self.model = AuditorModel(encoder_name)
        self.model.load_state_dict(torch.load(model_path, map_location="cpu"))
        self.model.eval()

    @torch.no_grad()
    def audit(self, text: str):
        tokens = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
        )

        out = self.model(**tokens)

        label_probs = out["label_probs"].squeeze(0)
        labels = {
            RISK_LABELS[i]: float(label_probs[i].item())
            for i in range(len(RISK_LABELS))
        }

        entropy = -(label_probs * torch.log(label_probs + 1e-6)).mean().item()

        return {
            "risk_score": float(out["risk_score"].item()),
            "risk_labels": labels,
            "uncertainty": entropy,
        }
