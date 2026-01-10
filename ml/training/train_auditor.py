import torch
import tqdm
from torch.utils.data import DataLoader
from ml.models.auditor_model import AuditorModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def train_auditor(dataset, encoder_name: str):
    model = AuditorModel(encoder_name).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5, weight_decay=0.01)

    bce = torch.nn.BCELoss()
    mse = torch.nn.MSELoss()

    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    model.train()
    for epoch in range(10):
        epoch_loss = 0
        loop = tqdm.tqdm(loader, desc=f"Epoch {epoch}")
        for batch in loop:
            batch = {k: v.to(device) for k, v in batch.items()}
            
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

            epoch_loss += loss.item()
            loop.set_postfix(loss=loss.item())

        print(f"Epoch {epoch}: loss={epoch_loss / len(loader):.4f}")

    return model
