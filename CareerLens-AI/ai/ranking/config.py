"""Ranking configuration for CareerLens AI.

This module defines the weight settings used by the ranking engine. It
encapsulates default weights, normalization, and safe construction from raw
input so the ranking algorithm can stay simple and consistent.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_SEMANTIC_WEIGHT = 0.5
DEFAULT_RESUME_QUALITY_WEIGHT = 0.2
DEFAULT_ATS_WEIGHT = 0.15
DEFAULT_EXPERIENCE_WEIGHT = 0.1
DEFAULT_PROJECT_WEIGHT = 0.05


@dataclass(frozen=True)
class RankingConfig:
    """Configuration for candidate ranking weights."""

    semantic_weight: float = DEFAULT_SEMANTIC_WEIGHT
    resume_quality_weight: float = DEFAULT_RESUME_QUALITY_WEIGHT
    ats_weight: float = DEFAULT_ATS_WEIGHT
    experience_weight: float = DEFAULT_EXPERIENCE_WEIGHT
    project_weight: float = DEFAULT_PROJECT_WEIGHT

    @classmethod
    def from_dict(cls, config: dict[str, Any] | None) -> "RankingConfig":
        """Create a RankingConfig from a dictionary of raw values."""
        if not isinstance(config, dict):
            logger.debug("RankingConfig received invalid config; using defaults.")
            return cls()

        return cls(
            semantic_weight=_to_positive_float(config.get("semantic_weight"), DEFAULT_SEMANTIC_WEIGHT),
            resume_quality_weight=_to_positive_float(config.get("resume_quality_weight"), DEFAULT_RESUME_QUALITY_WEIGHT),
            ats_weight=_to_positive_float(config.get("ats_weight"), DEFAULT_ATS_WEIGHT),
            experience_weight=_to_positive_float(config.get("experience_weight"), DEFAULT_EXPERIENCE_WEIGHT),
            project_weight=_to_positive_float(config.get("project_weight"), DEFAULT_PROJECT_WEIGHT),
        )

    def normalized_weights(self) -> tuple[float, float, float, float, float]:
        """Return the normalized weight distribution for ranking."""
        total = (
            self.semantic_weight
            + self.resume_quality_weight
            + self.ats_weight
            + self.experience_weight
            + self.project_weight
        )
        if total <= 0:
            logger.warning("RankingConfig weights sum to zero or negative; falling back to defaults.")
            return (
                DEFAULT_SEMANTIC_WEIGHT,
                DEFAULT_RESUME_QUALITY_WEIGHT,
                DEFAULT_ATS_WEIGHT,
                DEFAULT_EXPERIENCE_WEIGHT,
                DEFAULT_PROJECT_WEIGHT,
            )

        return (
            self.semantic_weight / total,
            self.resume_quality_weight / total,
            self.ats_weight / total,
            self.experience_weight / total,
            self.project_weight / total,
        )


def _to_positive_float(value: Any, default: float) -> float:
    """Convert a raw value to a non-negative float, falling back to default."""
    try:
        number = float(value)
        if number < 0:
            logger.warning("RankingConfig received negative weight %s; using default %s.", value, default)
            return default
        return number
    except (TypeError, ValueError):
        logger.debug("RankingConfig received non-numeric weight %r; using default %s.", value, default)
        return default
