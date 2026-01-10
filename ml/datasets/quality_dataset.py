import torch
from torch.utils.data import Dataset


class QualityDataset(Dataset):
    def __init__(self, samples):
        self.samples = samples

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        s = self.samples[idx]
        return {
            "text": s["text"],
            "informativeness": torch.tensor(s["informativeness"]),
            "clarity": torch.tensor(s["clarity"]),
            "completeness": torch.tensor(s["completeness"]),
            "persuasion": torch.tensor(s["persuasion"]),
        }
