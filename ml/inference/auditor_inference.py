import torch
from sentence_transformers import SentenceTransformer
from ml.models.auditor_model import AuditorModel, RISK_LABELS

class AuditorAgent:
    def __init__(self, model_path: str, encoder_name: str):
        self.encoder = SentenceTransformer(encoder_name)
        self.model = AuditorModel()
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    def audit(self, text: str):
        embedding = self.encoder.encode([text], convert_to_tensor=True)

        out = mc_dropout_predict(self.model, embedding)

        label_probs = out["label_probs"].squeeze(0)
        labels = {
            RISK_LABELS[i]: float(label_probs[i].item())
            for i in range(len(RISK_LABELS))
        }

        return {
            "risk_score": float(out["risk_score"].item()),
            "risk_labels": labels,
            "uncertainty": float(out["uncertainty"][0])
        }
    

@torch.no_grad()
def mc_dropout_predict(model, embeddings, n_samples: int = 10):
    model.train()

    label_preds = []
    score_preds = []

    for _ in range(n_samples):
        out = model(embeddings)
        label_preds.append(out["label_probs"])
        score_preds.append(out["risk_score"])

    label_stack = torch.stack(label_preds)
    score_stack = torch.stack(score_preds)

    label_mean = label_stack.mean(dim=0)
    score_mean = score_stack.mean(dim=0)

    label_entropy = -(label_mean * torch.log(label_mean + 1e-6) +
                      (1 - label_mean) * torch.log(1 - label_mean + 1e-6)).mean(dim=1)

    score_var = score_stack.var(dim=0)

    uncertainty = (label_entropy + score_var).cpu().numpy()

    return {
        "label_probs": label_mean,
        "risk_score": score_mean,
        "uncertainty": uncertainty
    }
