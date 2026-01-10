import torch

from ml.datasets.quality_dataset import generate_quality_dataset
from ml.datasets.quality_dataset import QualityDataset
from ml.training.train_quality import train_quality_model

samples = generate_quality_dataset(3000)
dataset = QualityDataset(samples)

model = train_quality_model(
    dataset,
    encoder_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

torch.save(model.state_dict(), "quality.pt")
