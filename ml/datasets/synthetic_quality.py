import random

def make_quality_sample(kind: str):
    if kind == "good":
        text = "Продаю велосипед. Отличное состояние, использовался 6 месяцев. Причина продажи — покупка нового."
        scores = {
            "informativeness": random.uniform(0.7, 0.9),
            "clarity": random.uniform(0.7, 0.9),
            "completeness": random.uniform(0.7, 0.9),
            "persuasion": random.uniform(0.5, 0.8),
        }

    elif kind == "short":
        text = "Продам велосипед"
        scores = {
            "informativeness": random.uniform(0.2, 0.4),
            "clarity": random.uniform(0.6, 0.7),
            "completeness": random.uniform(0.2, 0.4),
            "persuasion": random.uniform(0.3, 0.4),
        }

    elif kind == "spam":
        text = "🔥🔥🔥 КУПИ СЕЙЧАС !!! 🔥🔥🔥"
        scores = {
            "informativeness": random.uniform(0.2, 0.4),
            "clarity": random.uniform(0.2, 0.4),
            "completeness": random.uniform(0.2, 0.4),
            "persuasion": random.uniform(0.7, 0.9),
        }

    else:  # bad
        text = "!!!"
        scores = {k: 0.1 for k in ["informativeness", "clarity", "completeness", "persuasion"]}

    return {
        "text": text,
        **scores
    }


def generate_quality_dataset(n=2000):
    kinds = ["good", "short", "spam", "bad"]
    return [make_quality_sample(random.choice(kinds)) for _ in range(n)]
