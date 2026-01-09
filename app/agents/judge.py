from typing import List, Tuple

from app.models.schemas import AgentIssue


class JudgeAgent:
    """
    Aggregates risk and quality scores and produces final verdict.
    Docstring for JudgeAgent
    """

    def __init__(
        self,
        alpha: float = 0.5,
        beta: float = 0.5,
        published_threshold: float = 0.7,
        revise_threshold: float = 0.4,
    ) -> None:
        if not abs(alpha + beta - 1.0) < 1e-6:
            raise ValueError("alpha + beta must eual 1.0")

        self.alpha = alpha
        self.beta = beta
        self.published_threshold = published_threshold
        self.revise_threshold = revise_threshold

    
    def aggregate(
        self,
        risk_score: float,
        quality_score: float,
        issues: List[AgentIssue],
    ) -> Tuple[float, str, List[AgentIssue]]:
        """
        Aggregate agent outputs into final score and verdict.
        Docstring for aggregate
        
        :param self: Description
        :param risk_score: Description
        :type risk_score: float
        :param quality_score: Description
        :type quality_score: float
        :param issues: Description
        :type issues: List[AgentIssue]
        :return: final_score, verdict, issues
        :rtype: Tuple[float, str, List[AgentIssue]]
        """
        final_score = self.alpha * (1.0 - risk_score) + self.beta * quality_score
        final_score = round(min(1.0, max(0.0, final_score)), 2)

        if final_score >= self.published_threshold:
            verdict = "publish"
        elif final_score >= self.revise_threshold:
            verdict = "revise"
        else:
            verdict = "reject"
        
        return final_score, verdict, issues
