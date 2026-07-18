"""Score calculator for CareerLens AI ranking engine.

This module computes the final normalized score for a candidate using only
results produced by previous modules. It applies configurable weights to
semantic similarity, resume quality, ATS score, experience relevance, and
project relevance.
"""

from __future__ import annotations

import logging
from typing import Any

from ai.ranking.config import RankingConfig

logger = logging.getLogger(__name__)


def calculate_candidate_score(candidate: dict[str, Any], config: RankingConfig | None = None) -> float:
    """Calculate the final ranking score for one candidate.

    Parameters
    ----------
    candidate:
        Dictionary containing candidate, analysis, and matching data.
    config:
        RankingConfig with normalized factor weights.

    Returns
    -------
    float
        Final score between 0.0 and 100.0.
    """
    if not isinstance(candidate, dict):
        logger.warning("calculate_candidate_score received invalid candidate input.")
        return 0.0

    analysis = candidate.get("analysis", {})
    matching = candidate.get("matching", {})

    semantic_similarity = _as_fraction(matching.get("semantic_similarity"))
    resume_score = _as_score(analysis.get("resume_score"))
    ats_score = _as_score(analysis.get("ats_score"))
    match_score = _as_score(matching.get("match_score"))

    experience_relevance = _as_fraction(
        matching.get("experience_relevance"),
        default=_as_fraction(match_score),
    )
    project_relevance = _as_fraction(
        matching.get("project_relevance"),
        default=_as_fraction(match_score),
    )

    semantic_weight, resume_quality_weight, ats_weight, experience_weight, project_weight = (
        config.normalized_weights()
    )

    final = (
        semantic_similarity * semantic_weight
        + _normalize_percentage(resume_score) * resume_quality_weight
        + _normalize_percentage(ats_score) * ats_weight
        + experience_relevance * experience_weight
        + project_relevance * project_weight
    )

    return round(max(0.0, min(100.0, final * 100.0)), 1)


def _as_score(value: Any) -> float:
    """Convert a value to a bounded score between 0 and 100."""
    try:
        score = float(value)
        if score < 0:
            return 0.0
        if score > 100:
            return 100.0
        return score
    except (TypeError, ValueError):
        return 0.0


def _as_fraction(value: Any, default: float = 0.0) -> float:
    """Convert a value to a bounded fraction between 0.0 and 1.0."""
    try:
        fraction = float(value)
        if fraction < 0.0:
            return 0.0
        if fraction > 1.0:
            return 1.0
        return fraction
    except (TypeError, ValueError):
        return _as_fraction(default, 0.0)


def _normalize_percentage(score: float) -> float:
    """Normalize a score from 0-100 into a fraction 0.0-1.0."""
    return max(0.0, min(1.0, score / 100.0))
