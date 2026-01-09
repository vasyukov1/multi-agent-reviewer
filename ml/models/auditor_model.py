import torch
import torch.nn as nn
import torch.nn.functional as F

RISK_LABELS = ["scam", "adult", "illegal", "spam", "low_info"]

class AuditorModel(nn.Module):
    def __init__(self, embedding_dim: int = 384, hidden_dim: int = 128):
        super().__init__()

        self.shared = nn.Sequential(
            nn.Linear(embedding_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )

        self.label_head = nn.Linear(hidden_dim, len(RISK_LABELS))
        self.score_head = nn.Linear(hidden_dim, 1)

    def forward(self, embeddings):
        x = self.shared(embeddings)

        label_logits = self.label_head(x)
        label_probs = torch.sigmoid(label_logits)

        risk_score = torch.sigmoid(self.score_head(x)).squeeze(-1)

        return {
            "label_probs": label_probs,
            "risk_score": risk_score
        }