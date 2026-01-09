import re
from typing import List, Tuple

from app.models.schemas import AdInput, AgentIssue


class AuditorAgent:
    """
    Docstring for AuditorAgent
    Rule-based content auditor.
    Detects risky patterns in ad text.
    """

    BANNED_WORDS = [
        "scam",
        "fraud",
        "подделка",
        "обман",
        "мошенничество",
        "fake",
        "копия",
    ]

    MIN_TITLE_LENGTH = 5
    MIN_DESCRIPTION_LENGTH = 20

    PHONE_REGEX = re.compile(
        r"(\+?\d[\d\s\-]{7,}\d)"
    )
    EMAIL_REGEX = re.compile(
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    )

    def analyze(self, ad: AdInput) -> Tuple[float, List[AgentIssue]]:
        """
        Docstring for analyze
        Analyze ad content and return (risk_score, issues).
        
        :param self: Description
        :param ad: Description
        :type ad: AdInput
        :return: Description
        :rtype: Tuple[float, List[AgentIssue]]
        """
        issues: List[AgentIssue] = []
        risk = 0.0

        text = f"{ad.title} {ad.description}".lower()

        # Banned words
        for word in self.BANNED_WORDS:
            if word in text:
                issues.append(
                    AgentIssue(
                        agent="auditor",
                        code="BANNED_WORD",
                        message=f"Detected banned word: {word}",
                        details={"word": word},
                    )
                )
                risk += 0.3

        # Minimal length check
        if len(ad.title) < self.MIN_TITLE_LENGTH:
            issues.append(
                AgentIssue(
                    agent="auditor",
                    code="TITLE_TOO_SHORT",
                    message="Title is too short",
                    details={"min_length": self.MIN_TITLE_LENGTH},
                )
            )
            risk += 0.2

        if len(ad.description) < self.MIN_DESCRIPTION_LENGTH:
            issues.append(
                AgentIssue(
                    agent="auditor",
                    code="DESCRIPTION_TOO_SHORT",
                    message="Description is too short",
                    details={"min_length": self.MIN_DESCRIPTION_LENGTH},
                )
            )
            risk += 0.2

        # Contact info detection
        if self.PHONE_REGEX.search(text):
            issues.append(
                AgentIssue(
                    agent="auditor",
                    code="PHONE_DETECTED",
                    message="Phone number detected in text",
                )
            )
            risk += 0.2
        
        if self.EMAIL_REGEX.search(text):
            issues.append(
                AgentIssue(
                    agent="auditor",
                    code="EMAIL_DETECTED",
                    message="Email detected in text",
                )
            )
            risk += 0.2


        # Clamp risk to [0, 1]
        risk = min(1.0, round(risk, 2))

        return risk, issues