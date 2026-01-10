import torch

from ml.datasets.judge_dataset import generate_judge_dataset
from ml.datasets.judge_dataset import JudgeDataset
from ml.training.train_judge import train_judge

X, y = generate_judge_dataset()
dataset = JudgeDataset(X, y)

model = train_judge(dataset, input_dim=X[0].shape[0])
torch.save(model.state_dict(), "judge_model.pt")
