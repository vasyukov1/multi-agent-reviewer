import json
import logging
from pathlib import Path
from typing import List, Tuple

import numpy as np

from app.models.schemas import AdInput, AgentIssue
from app.services.model_loader import EmbeddingModelLoader

logger = logging.getLogger(__name__)


class QualityAgent:
    """
    Quality scoring agent using heuristics + embedding similarity.
    Docstring for QualityAgent
    """

    def __init__(
        self,
        examples_path: str = "data/examples",
        model_loader: EmbeddingModelLoader | None = None,
    ) -> None:
        self.examples_path = Path(examples_path)
        self.model_loader = model_loader or EmbeddingModelLoader()
        self._example_embeddings: np.ndarray | None = None

    
    def load_examples(self) -> List[str]:
        """
        Load good-quality ad examples from data/examples.
        Docstring for load_examples
        
        :param self: Description
        :return: Description
        :rtype: List[str]
        """
        texts: List[str] = []

        for file in self.examples_path.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                text = f"{data['title']} {data['description']}"
                texts.append(text)

        if not texts:
            raise RuntimeError("No quality examples found")

        return texts
    

    def _ensure_example_embeddings(self) -> None:
        if self._example_embeddings is None:
            examples = self.load_examples()
            embeddings = self.model_loader.get_embedding(examples)
            self._example_embeddings = np.array(embeddings)

    
    def _heuristicx_score(self, ad: AdInput) -> float:
        """
        Simple heuristic quality score in [0,1].
        Docstring for heuristic_score
        
        :param self: Description
        :param ad: Description
        :type ad: AdInput
        :return: Description
        :rtype: float
        """
        score = 0.0

        text = f"{ad.title} {ad.description}".lower()

        # Length heuristic
        if len(ad.description) >= 50:
            score += 0.3
        
        # Informative keywords
        keywords = ["состояние", "новый", "б/у", "оригинал", "brand", "model"]
        if any(k in text for k in keywords):
            score += 0.3

        # Category presence
        if ad.category:
            score += 0.2
        
        return min(1.0, score)
    

    def _similarity_score(self, ad: AdInput) -> float:
        """
        Cosine similarity against good examples, normalized to [0,1].
        Docstring for _similarity_score
        
        :param self: Description
        :param ad: Description
        :type ad: AdInput
        :return: Description
        :rtype: float
        """
        self._ensure_example_embeddings()

        query_text = f"{ad.title} {ad.description}".lower()
        query_embedding = np.array(self.model_loader.get_embedding([query_text])[0])

        sims = np.dot(self._example_embeddings, query_embedding)
        max_sim = float(np.max(sims))

        return max(0.0, min(1.0, max_sim))
    

    def analyze(self, ad: AdInput) -> Tuple[float, List[AgentIssue]]:
        """
        Analyze ad quality and return (quality_score, issues).
        Docstring for analyze
        
        :param self: Description
        :param ad: Description
        :type ad: AdInput
        :return: Description
        :rtype: Tuple[float, List[AgentIssue]]
        """
        issues: List[AgentIssue] = []

        heuristics_score = self._heuristicx_score(ad)
        similarity_score = self._similarity_score(ad)

        quality_score = round(0.5 * heuristics_score + 0.5 * similarity_score, 3)

        if quality_score < 0.4:
            issues.append(
                AgentIssue(
                    agent="quality",
                    code="LOW_QUALITY",
                    message="Ad quality is below recommended threshold",
                    details={
                        "heuristics_score": heuristics_score,
                        "similarity_score": similarity_score,
                    },
                )
            )

        return quality_score, issues
