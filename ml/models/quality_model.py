import torch
import torch.nn as nn
from transformers import AutoModel


class QualityModel(nn.Module):
    def __init__(self, encoder_name: str, hidden_dim: int = 256):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(encoder_name)
        emb_dim = self.encoder.config.hidden_size

        self.shared = nn.Sequential(
            nn.Linear(emb_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
        )

        self.heads = nn.ModuleDict({
            "informativeness": nn.Linear(hidden_dim, 1),
            "clarity": nn.Linear(hidden_dim, 1),
            "completeness": nn.Linear(hidden_dim, 1),
            "persuasion": nn.Linear(hidden_dim, 1),
        })

    def forward(self, input_ids, attention_mask):
        out = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        pooled = out.last_hidden_state[:, 0]
        shared = self.shared(pooled)

        aspects = {
            name: torch.sigmoid(head(shared)).squeeze(-1)
            for name, head in self.heads.items()
        }

        quality_score = torch.stack(list(aspects.values()), dim=1).mean(dim=1)

        return {
            "quality_score": quality_score,
            "aspects": aspects
        }
