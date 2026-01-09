import logging
from typing import List

import torch
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class EmbeddingModelLoader:
    """
    Docstring for EmbeddingModelLoader
    Wrapper for sentence-transformers embedding model.
    """

    def __init__(
        self,
        model_name: str = "paraphrase-multilingual-MiniLM-L12-v2",
        device: str | None = None,
    ) -> None:
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self._model: SentenceTransformer | None = None

    
    def load(self) -> None:
        """
        Load model into memory.
        Docstring for load
        
        :param self: Description
        """
        if self._model is None:
            logger.info(
                "Loading embedding model",
                extra={
                    "model": self.model_name, 
                    "device": self.device,
                },
            )
            self._model = SentenceTransformer(self.model_name, self.device)


    @property
    def is_loaded(self) -> bool:
        return self._model is not None
    

    def get_embedding(self, texts: List[str]) -> List[List[float]]:
        """
        Compute embeddings for a list of texts.
        Docstring for get_embedding
        
        :param self: Description
        :param texts: Description
        :type texts: List[str]
        :return: Description
        :rtype: List[List[float]]
        """
        if self._model is None:
            self.load()

        try:
            embeddings = self._model.encode(
                texts,
                normalize_embeddings=True,
                convert_to_numpy=True,
                show_progress_bar=False,
            )
            return embeddings.tolist()
        except Exception as e:
            logger.exception("Embedding computation failed")
            raise RuntimeError("Embedding computation failed") from e