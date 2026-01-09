import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from app.models.schemas import AdInput, ReviewResult


class ReviewPersistence:
    """
    File-based persistence for review results.
    Docstring for ReviewPersistence
    """

    def __init__(self, base_path="data/results") -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(
        self,
        ad: AdInput,
        result: ReviewResult,
    ) -> Path:
        """
        Save review input and result to JSON file.
        Docstring for save
        
        :param self: Description
        :param ad: Description
        :type ad: AdInput
        :param result: Description
        :type result: ReviewResult
        :return: Path to saved file
        :rtype: Path
        """
        payload: Dict[str, Any] = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "input": ad.model_dump(),
            "result": result.model_dump(),
        }

        filename = f"{payload['timestamp']}_{payload['id']}.json"
        filepath = self.base_path / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        return filepath
