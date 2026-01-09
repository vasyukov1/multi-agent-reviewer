import numpy as np


def build_judge_features(auditor, quality, meta=None):
    features = [
        auditor["risk_score"],
        auditor.get("uncertainty", 0.0),
        quality["quality_score"],
        quality.get("confidence", 1.0),
    ]

    # Quality aspects
    for k in ["informativeness", "clarity", "completeness", "persuasion"]:
        features.append(quality["aspects"].get(k, 0.0))

    # Optional meta-features
    if meta:
        features.append(meta.get("text_length", 0) / 1000)
        features.append(meta.get("embedding_norm", 0.0))

    return np.array(features, dtype="float32")
