import torch
from torch.utils.data import DataLoader
from ml.models.auditor_model import AuditorModel


def train_auditor(dataset, embedding_dim: int = 384):
    model = AuditorModel(embedding_dim)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

    bce = torch.nn.BCELoss()
    mse = torch.nn.MSELoss()

    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    model.train()
    for epoch in range(10):
        for emb, labels, score in loader:
            out = model(emb)

            loss_labels = bce(out["label_probs"], labels)
            loss_score = mse(out["risk_score"], score)

            loss = loss_labels + loss_score

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch}: loss={loss.item():.4f}")

    return model
