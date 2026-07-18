"""Embedding service for CareerLens AI matcher.

This module provides a single responsibility: load a Sentence Transformers model
once and encode text into embeddings usable by later semantic similarity layers.
It is intentionally minimal so the matcher architecture can remain modular and
future-proof.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any, Protocol

import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"


class EmbeddingService(Protocol):
    """Protocol defining the embedding service interface."""

    def encode(self, texts: list[str]) -> np.ndarray:
        ...


class SentenceTransformerEmbeddingService:
    """Sentence Transformers wrapper that caches the loaded model."""

    def __init__(self, model_name: str = DEFAULT_EMBEDDING_MODEL) -> None:
        self.model_name = model_name
        self._model: SentenceTransformer | None = None

    def encode(self, texts: list[str]) -> np.ndarray:
        """Encode a list of strings into a NumPy embedding matrix."""
        if not isinstance(texts, list):
            logger.warning("EmbeddingService.encode received non-list input.")
            return np.empty((0, 0), dtype=float)

        normalized_texts = self._normalize_texts(texts)
        if not normalized_texts:
            return np.empty((0, 0), dtype=float)

        model = self._get_model()
        try:
            embeddings = model.encode(normalized_texts, convert_to_numpy=True)
            return np.asarray(embeddings, dtype=float)
        except Exception as error:
            logger.exception("Failed to encode texts with SentenceTransformer.")
            return np.empty((0, 0), dtype=float)

    def _get_model(self) -> SentenceTransformer:
        if self._model is None:
            logger.info("Loading embedding model '%s'", self.model_name)
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def _normalize_texts(self, texts: list[Any]) -> list[str]:
        normalized: list[str] = []
        for item in texts:
            if isinstance(item, str):
                text = item.strip()
                if text:
                    normalized.append(text)
            else:
                logger.warning("EmbeddingService.encode ignored non-string item: %r", item)
        return normalized


@lru_cache(maxsize=4)
def get_embedding_service(model_name: str = DEFAULT_EMBEDDING_MODEL) -> SentenceTransformerEmbeddingService:
    """Return a cached embedding service for the requested model."""
    return SentenceTransformerEmbeddingService(model_name)
