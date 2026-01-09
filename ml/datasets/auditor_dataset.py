from dataclasses import dataclass
from typing import List
import torch
from torch.utils.data import Dataset


@dataclass
class AuditorSample:
    text: str
    risk_score: float       # [0, 1] noisy
    risk_labels: List[int]  # multi-hot
    source: str             # rule / synthetic / self_train


class AuditorDataset(Dataset):
    def __init__(self, samples: List[AuditorSample], tokenizer, max_len: int = 256):
        self.samples = samples
        self.tokenizer = tokenizer
        self.max_len = max_len
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        s = self.samples[idx]
        enc = self.tokenizer(
            s.text,
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_tensors="pt",
        )

        return {
            "input_ids": enc["input_ids"].squeeze(0),
            "attention_mask": enc["attention_mask"].squeeze(0),
            "risk_score": torch.tensor(s.risk_score, dtype=torch.float),
            "risk_labels": torch.tensor(s.risk_labels, dtype=torch.float),
        }
