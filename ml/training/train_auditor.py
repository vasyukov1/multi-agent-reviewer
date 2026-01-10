import torch
from torch.utils.data import DataLoader
from ml.models.auditor_model import AuditorModel


def train_auditor(dataset, encoder_name: str):
    model = AuditorModel(encoder_name)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

    bce = torch.nn.BCELoss()
    mse = torch.nn.MSELoss()

    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    model.train()
    for epoch in range(10):
        for batch in loader:
            out = model(
                input_ids=batch["input_ids"],
                attention_mask=batch["attention_mask"],
            )

            loss_labels = bce(out["label_probs"], batch["risk_labels"])
            loss_score = mse(out["risk_score"], batch["risk_score"])

            loss = loss_labels + loss_score

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch}: loss={loss.item():.4f}")

    return model
