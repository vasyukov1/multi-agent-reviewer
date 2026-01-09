import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer
from ml.models.quality_model import QualityModel


def train_quality_model(dataset, encoder_name: str):
    tokenizer = AutoTokenizer.from_pretrained(encoder_name)
    model = QualityModel(encoder_name)
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
    criterion = torch.nn.MSELoss()

    loader = DataLoader(dataset, batch_size=16, shuffle=True)

    model.train()
    for epoch in range(3):
        for batch in loader:
            tokens = tokenizer(
                batch["text"],
                padding=True,
                truncation=True,
                return_tensors="pt",
            )

            out = model(**tokens)

            loss = 0.0
            for aspect, pred in out["aspects"].items():
                loss += criterion(pred, batch[aspect])

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch} loss: {loss.item():.4f}")

    return model
