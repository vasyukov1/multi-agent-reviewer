import torch
from torch.utils.data import DataLoader
from ml.models.judge_model import JudgeModel


def train_judge(dataset, input_dim: int):
    model = JudgeModel(input_dim=input_dim)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    criterion = torch.nn.CrossEntropyLoss()

    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    model.train()
    for epoch in range(10):
        for x, y in loader:
            out = model(x)
            loss = criterion(out["logits"], y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch}: loss={loss.item():.4f}")

    return model
