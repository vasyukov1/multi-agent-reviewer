from app.agents.auditor import AuditorAgent
from app.models.schemas import AdInput


def test_good_ad_low_risk():
    agent = AuditorAgent()
    ad = AdInput(
        title="Продам велосипед",
        description="Отличный горный велосипед, почти не использовался, состояние идеальное.",
        category="sport",
    )

    risk, issues = agent.analyze(ad)

    assert risk == 0.0
    assert issues == []


def test_short_ad_high_risk():
    agent = AuditorAgent()
    ad = AdInput(
        title="$$$",
        description="Хороший",
    )

    risk, issues = agent.analyze(ad)

    codes = {issue.code for issue in issues}

    assert "TITLE_TOO_SHORT" in codes
    assert "DESCRIPTION_TOO_SHORT" in codes
    assert risk >= 0.4


def test_banned_word_and_contact():
    agent = AuditorAgent()
    ad = AdInput(
        title="Cheap iPhone",
        description="This is not a scam, write to me at test@example.com or +123456789",
    )

    risk, issues = agent.analyze(ad)

    codes = {issue.code for issue in issues}

    assert "BANNED_WORD" in codes
    assert "PHONE_DETECTED" in codes
    assert "EMAIL_DETECTED" in codes
    assert risk > 0.5