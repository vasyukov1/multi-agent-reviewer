import random

SCAM_PHRASES = [
    "гарантированный доход",
    "переведите предоплату",
    "инвестиции без риска",
    "срочно, только сегодня"
]

LOW_INFO_TITLES = ["Продам", "Хорошее", "Отдам"]
SPAM_TOKENS = ["🔥🔥🔥", "!!!", "ТОЛЬКО СЕЙЧАС"]

NORMAL_TEMPLATES = [
    "Продаю {item}. Состояние {condition}. Использовался {time}. Причина продажи — {reason}."
]

ITEMS = ["велосипед", "телефон", "ноутбук"]
CONDITIONS = ["отличное", "хорошее"]
TIMES = ["1 год", "6 месяцев"]
REASONS = ["покупка нового", "не используется"]


def generate_ad(label: str) -> dict:
    if label == "scam":
        text = f"{random.choice(SCAM_PHRASES)} {random.choice(SCAM_PHRASES)}"
    elif label == "low_info":
        text = random.choice(LOW_INFO_TITLES)
    elif label == "spam":
        text = f"{random.choice(SPAM_TOKENS)} Купить {random.choice(SPAM_TOKENS)}"
    else:
        text = random.choice(NORMAL_TEMPLATES).format(
            item=random.choice(ITEMS),
            condition=random.choice(CONDITIONS),
            time=random.choice(TIMES),
            reason=random.choice(REASONS),
        )

    return {
        "text": text,
        "label": label
    }


def generate_dataset(n: int = 1000):
    labels = ["normal", "scam", "low_info", "spam"]
    return [generate_ad(random.choice(labels)) for _ in range(n)]
