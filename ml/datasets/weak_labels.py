from ml.models.auditor_model import RISK_LABELS

def weak_label(text: str):
    labels = {
        "scam": int("гарантир" in text or "предоплат" in text),
        "spam": int(text.count("!") > 2),
        "low_info": int(len(text) < 20),
        "adult": 0,
        "illegal": 0,
    }

    multi_hot = [labels[k] for k in RISK_LABELS]
    risk_score = float(max(multi_hot))

    return labels, risk_score
