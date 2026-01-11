import torch
from typing import List
from transformers import AutoTokenizer

from ..datasets.synthetic_auditor import generate_dataset
from ..datasets.weak_labels import weak_label
from ..datasets.auditor_dataset import AuditorSample, AuditorDataset
from ..training.train_auditor import train_auditor

ENCODER = "distilbert-base-multilingual-cased"

tokenizer = AutoTokenizer.from_pretrained(ENCODER)

raws = generate_dataset(5000)

samples: List[AuditorSample] = []
for raw in raws:
    text = raw["text"]
    labels, score = weak_label(text)

    sample = AuditorSample(
        text=text,
        risk_score=score,
        risk_labels=labels,
        source="synthetic",
    )
    samples.append(sample)

dataset = AuditorDataset(samples, tokenizer)
model = train_auditor(dataset, ENCODER)

torch.save(model.state_dict(), "auditor.pt")
