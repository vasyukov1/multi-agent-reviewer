import torch
import torch.nn as nn
from transformers import AutoModel

RISK_LABELS = ["scam", "adult", "illegal", "spam", "low_info"]


class AuditorModel(nn.Module):
    def __init__(self, encoder_name: str, hidden_dim: int = 128):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(encoder_name)
        emb_dim = self.encoder.config.hidden_size

        self.shared = nn.Sequential(
            nn.Linear(emb_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
        )

        self.label_head = nn.Linear(hidden_dim, len(RISK_LABELS))
        self.score_head = nn.Linear(hidden_dim, 1)

    def forward(self, input_ids, attention_mask):
        out = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask,
        )
        pooled = out.last_hidden_state[:, 0]
        shared = self.shared(pooled)

        label_probs = torch.sigmoid(self.label_head(shared))
        risk_score = torch.sigmoid(self.score_head(shared)).squeeze(-1)

        return {
            "label_probs": label_probs,
            "risk_score": risk_score
        }
