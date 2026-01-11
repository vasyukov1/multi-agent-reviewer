import torch
import torch.nn as nn
import torch.nn.functional as F


class JudgeModel(nn.Module):
    def __init__(
        self,
        input_dim: int,
        hidden_dim: int = 64,
        num_classes: int = 3
    ):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, num_classes)
        )

    def forward(self, x):
        logits = self.net(x)
        probs = F.softmax(logits, dim=-1)

        return {
            "logits": logits,
            "probs": probs
        }
