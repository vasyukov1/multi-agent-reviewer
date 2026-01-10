import random
import numpy as np

VERDICTS = {"publish": 0, "revise": 1, "reject": 2}

def generate_judge_sample():
    risk = random.random()
    uncertainty = random.random() * 0.3
    quality = random.random()

    aspects = [random.uniform(0.3, 1.0) for _ in range(4)]

    features = [
        risk,
        uncertainty,
        quality,
        1 - np.std(aspects),
        *aspects
    ]

    if risk > 0.7:
        label = VERDICTS["reject"]
    elif risk < 0.3 and quality > 0.7:
        label = VERDICTS["publish"]
    else:
        label = VERDICTS["revise"]

    return np.array(features, dtype="float32"), label


def generate_judge_dataset(n=5000):
    X, y = [], []
    for _ in range(n):
        f, l = generate_judge_sample()
        X.append(f)
        y.append(l)
    return X, y
