import numpy as np
from ml.features.judge_features import build_judge_features
from ml.models.auditor_model import RISK_LABELS

VERDICTS = {"publish": 0, "revise": 1, "reject": 2}

def generate_fake_auditor():
    risk = np.random.beta(2, 5)
    label_probs = np.random.dirichlet(np.ones(len(RISK_LABELS)))
    entropy = -(label_probs * np.log(label_probs + 1e-8)).sum()

    return {
        "risk_score": float(risk),
        "risk_labels": dict(zip(RISK_LABELS, label_probs)),
        "uncertainty": float(entropy)
    }


def generate_fake_quality():
    aspects = {
        "informativeness": np.random.uniform(0.2, 1.0),
        "clarity": np.random.uniform(0.2, 1.0),
        "completeness": np.random.uniform(0.2, 1.0),
        "persuasion": np.random.uniform(0.2, 1.0),
    }

    quality = np.mean(list(aspects.values()))
    confidence = 1 - np.std(list(aspects.values()))

    return {
        "quality_score": float(quality),
        "aspects": aspects,
        "confidence": float(confidence)
    }


def generate_judge_sample():
    auditor = generate_fake_auditor()
    quality = generate_fake_quality()

    meta = {
        "text_length": np.random.randint(20, 2000),
        "embedding_norm": np.random.uniform(5, 15)
    }

    features = build_judge_features(auditor, quality, meta)

    if auditor["risk_score"] > 0.7:
        label = VERDICTS["reject"]
    elif quality["quality_score"] > 0.75 and auditor["risk_score"] < 0.3:
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
