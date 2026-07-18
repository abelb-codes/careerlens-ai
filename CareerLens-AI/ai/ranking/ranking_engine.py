"""Candidate ranking engine for CareerLens AI.

This module ranks candidate records produced by analysis and matching
pipelines. It converts raw candidate artifacts into a stable, sorted ranking
list containing final scores and the key factors used to derive each rank.
"""

from __future__ import annotations

import logging
from typing import Any

from ai.ranking.config import RankingConfig
from ai.ranking.score_calculator import calculate_candidate_score

logger = logging.getLogger(__name__)


def rank_candidates(
    candidates: list[dict[str, Any]] | None,
    config: dict[str, Any] | RankingConfig | None = None,
) -> list[dict[str, Any]]:
    """Rank candidates by final score using configurable ranking weights."""
    if not isinstance(candidates, list):
        logger.warning("rank_candidates received invalid candidate list input.")
        return []

    ranking_config = (
        config
        if isinstance(config, RankingConfig)
        else RankingConfig.from_dict(config if isinstance(config, dict) else None)
    )

    ranked_candidates: list[dict[str, Any]] = []
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            logger.warning("rank_candidates skipped invalid candidate at index %s.", index)
            continue

        final_score = calculate_candidate_score(candidate, ranking_config)
        ranking_record = {
            "rank": 0,
            "candidate_name": _get_candidate_name(candidate),
            "final_score": final_score,
            "resume_score": _as_score(candidate.get("analysis", {}).get("resume_score")),
            "ats_score": _as_score(candidate.get("analysis", {}).get("ats_score")),
            "match_score": _as_score(candidate.get("matching", {}).get("match_score")),
            "source_index": index,
        }
        ranked_candidates.append(ranking_record)

    ranked_candidates.sort(key=lambda record: (-record["final_score"], record["source_index"]))

    current_rank = 1
    previous_score: float | None = None
    for position, record in enumerate(ranked_candidates, start=1):
        if previous_score is not None and record["final_score"] < previous_score:
            current_rank = position

        record["rank"] = current_rank
        previous_score = record["final_score"]
        record.pop("source_index", None)

    return ranked_candidates


def _get_candidate_name(candidate: dict[str, Any]) -> str:
    """Extract a best-effort candidate name from a candidate record."""
    sources = (
        candidate.get("name"),
        candidate.get("candidate_name"),
        candidate.get("resume_profile", {}).get("name") if isinstance(candidate.get("resume_profile"), dict) else None,
        candidate.get("profile", {}).get("name") if isinstance(candidate.get("profile"), dict) else None,
        candidate.get("analysis", {}).get("name") if isinstance(candidate.get("analysis"), dict) else None,
        candidate.get("extracted_resume", {}).get("name") if isinstance(candidate.get("extracted_resume"), dict) else None,
    )

    for source in sources:
        if isinstance(source, str) and source.strip():
            return source.strip()

    return "Unknown Candidate"


def _as_score(value: Any) -> int:
    """Convert a value to an integer score between 0 and 100."""
    try:
        score = int(float(value))
    except (TypeError, ValueError):
        return 0

    if score < 0:
        return 0
    if score > 100:
        return 100
    return score
