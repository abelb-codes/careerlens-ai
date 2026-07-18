"""Similarity utilities for CareerLens AI matcher.

This module is responsible for semantic similarity computation and term-based
coverage comparisons. It separates vector math from the matching engine and
keeps the matcher architecture clean and testable.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


def compute_semantic_similarity(embeddings: np.ndarray) -> float:
    """Compute cosine similarity between two embedding vectors.

    Parameters
    ----------
    embeddings:
        A NumPy array containing exactly two embedding vectors as rows.

    Returns
    -------
    float
        A similarity score between 0.0 and 1.0.
    """
    if not isinstance(embeddings, np.ndarray):
        logger.warning("compute_semantic_similarity received non-ndarray input.")
        return 0.0

    if embeddings.ndim != 2 or embeddings.shape[0] != 2:
        logger.warning(
            "compute_semantic_similarity requires a 2D array of shape (2, dim); got %s.",
            embeddings.shape,
        )
        return 0.0

    try:
        similarity = cosine_similarity(embeddings[0].reshape(1, -1), embeddings[1].reshape(1, -1))
        score = float(np.nan_to_num(similarity[0, 0], nan=0.0))
        return max(0.0, min(1.0, score))
    except Exception as error:  # pragma: no cover
        logger.exception("Failed to compute cosine similarity.")
        return 0.0


def compare_term_sets(
    required_terms: Any, candidate_terms: Any
) -> tuple[list[str], list[str]]:
    """Compare required terms with candidate terms and return matched/missing lists."""
    normalized_required = _normalize_terms(required_terms)
    normalized_candidate = _normalize_terms(candidate_terms)

    matched: list[str] = []
    missing: list[str] = []

    for term in normalized_required:
        if term in normalized_candidate:
            matched.append(term)
        else:
            missing.append(term)

    return matched, missing


def coverage_ratio(required_terms: Any, matched_terms: list[str]) -> float:
    """Return the ratio of matched terms to required terms."""
    normalized_required = _normalize_terms(required_terms)
    if not normalized_required:
        return 1.0

    return len(matched_terms) / len(normalized_required)


def _normalize_terms(value: Any) -> list[str]:
    """Normalize term sets to lowercase strings."""
    if isinstance(value, str):
        text = value.strip().lower()
        return [text] if text else []

    if isinstance(value, list):
        normalized: list[str] = []
        for item in value:
            if isinstance(item, str):
                term = item.strip().lower()
                if term:
                    normalized.append(term)
            else:
                logger.warning("compare_term_sets ignored non-string item: %r", item)
        return normalized

    return []
