"""Matching engine for CareerLens AI.

This module orchestrates resume-job semantic matching using embeddings,
cosine similarity, skill coverage, keyword overlap, and experience relevance.
It produces a stable output contract for downstream consumption by Django and
other integration layers.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

from ai.matcher.embedding_service import EmbeddingService, get_embedding_service
from ai.matcher.similarity import (
    compute_semantic_similarity,
    compare_term_sets,
    coverage_ratio,
)

logger = logging.getLogger(__name__)

DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"
DEFAULT_SEMANTIC_WEIGHT = 0.5
DEFAULT_SKILL_WEIGHT = 0.25
DEFAULT_KEYWORD_WEIGHT = 0.15
DEFAULT_EXPERIENCE_WEIGHT = 0.1


class MatchEngineConfig:
    """Configuration for the matching engine."""

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_NAME,
        semantic_weight: float = DEFAULT_SEMANTIC_WEIGHT,
        skill_weight: float = DEFAULT_SKILL_WEIGHT,
        keyword_weight: float = DEFAULT_KEYWORD_WEIGHT,
        experience_weight: float = DEFAULT_EXPERIENCE_WEIGHT,
    ) -> None:
        self.model_name = model_name
        self.semantic_weight = semantic_weight
        self.skill_weight = skill_weight
        self.keyword_weight = keyword_weight
        self.experience_weight = experience_weight

    def normalized_weights(self) -> tuple[float, float, float, float]:
        total = (
            self.semantic_weight
            + self.skill_weight
            + self.keyword_weight
            + self.experience_weight
        )
        if total <= 0:
            return (
                DEFAULT_SEMANTIC_WEIGHT,
                DEFAULT_SKILL_WEIGHT,
                DEFAULT_KEYWORD_WEIGHT,
                DEFAULT_EXPERIENCE_WEIGHT,
            )
        return (
            self.semantic_weight / total,
            self.skill_weight / total,
            self.keyword_weight / total,
            self.experience_weight / total,
        )


def match_resume_to_job(
    resume_profile: dict[str, Any],
    job_profile: dict[str, Any],
    config: dict[str, Any] | None = None,
    embedding_provider: EmbeddingService | None = None,
) -> dict[str, Any]:
    """Match a parsed resume profile to a parsed job profile.

    Parameters
    ----------
    resume_profile:
        Resume profile dictionary produced by the extractor contract.
    job_profile:
        Job profile dictionary produced by the JD parser.
    config:
        Optional configuration values for model and scoring weights.
    embedding_provider:
        Optional embedding provider for dependency injection.

    Returns
    -------
    dict[str, Any]
        Matching output with score, similarity, matched skills, and keywords.
    """
    if not isinstance(resume_profile, dict) or not isinstance(job_profile, dict):
        logger.warning("Matching engine received invalid profile input.")
        return _empty_match_result()

    engine_config = _build_config(config)
    provider = embedding_provider or get_embedding_service(engine_config.model_name)

    resume_text = _build_resume_text(resume_profile)
    job_text = _build_job_text(job_profile)
    embeddings = provider.encode([resume_text, job_text])

    semantic_similarity = compute_semantic_similarity(embeddings)
    matched_skills, missing_skills = compare_term_sets(
        job_profile.get("required_skills"), resume_profile.get("skills")
    )
    matched_keywords, missing_keywords = compare_term_sets(
        job_profile.get("keywords"), resume_profile.get("projects")
    )
    experience_relevance = _calculate_experience_relevance(
        resume_profile.get("experience"),
        resume_profile.get("education"),
        job_profile.get("experience_required"),
        job_profile.get("education_required"),
    )

    semantic_weight, skill_weight, keyword_weight, experience_weight = (
        engine_config.normalized_weights()
    )

    match_score = _calculate_match_score(
        semantic_similarity=semantic_similarity,
        skill_coverage=coverage_ratio(job_profile.get("required_skills"), matched_skills),
        keyword_coverage=coverage_ratio(job_profile.get("keywords"), matched_keywords),
        experience_relevance=experience_relevance,
        semantic_weight=semantic_weight,
        skill_weight=skill_weight,
        keyword_weight=keyword_weight,
        experience_weight=experience_weight,
    )

    return {
        "match_score": match_score,
        "semantic_similarity": semantic_similarity,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
    }


def _empty_match_result() -> dict[str, Any]:
    return {
        "match_score": 0,
        "semantic_similarity": 0.0,
        "matched_skills": [],
        "missing_skills": [],
        "matched_keywords": [],
        "missing_keywords": [],
    }


def _build_config(config: dict[str, Any] | None) -> MatchEngineConfig:
    if not isinstance(config, dict):
        return MatchEngineConfig()

    return MatchEngineConfig(
        model_name=str(config.get("model_name", DEFAULT_MODEL_NAME)),
        semantic_weight=float(config.get("semantic_weight", DEFAULT_SEMANTIC_WEIGHT)),
        skill_weight=float(config.get("skill_weight", DEFAULT_SKILL_WEIGHT)),
        keyword_weight=float(config.get("keyword_weight", DEFAULT_KEYWORD_WEIGHT)),
        experience_weight=float(config.get("experience_weight", DEFAULT_EXPERIENCE_WEIGHT)),
    )


def _build_resume_text(resume_profile: dict[str, Any]) -> str:
    fields = (
        resume_profile.get("skills"),
        resume_profile.get("experience"),
        resume_profile.get("projects"),
        resume_profile.get("certifications"),
        resume_profile.get("languages"),
    )
    return _join_profile_fields(fields)


def _build_job_text(job_profile: dict[str, Any]) -> str:
    fields = (
        job_profile.get("job_title"),
        job_profile.get("required_skills"),
        job_profile.get("experience_required"),
        job_profile.get("education_required"),
        job_profile.get("keywords"),
    )
    return _join_profile_fields(fields)


def _join_profile_fields(fields: tuple[Any, ...]) -> str:
    parts: list[str] = []
    for field in fields:
        if isinstance(field, str):
            text = field.strip()
            if text:
                parts.append(text)
        elif isinstance(field, list):
            for item in field:
                if isinstance(item, str):
                    text = item.strip()
                    if text:
                        parts.append(text)
    return " ".join(parts)


def _calculate_experience_relevance(
    resume_experience: Any,
    resume_education: Any,
    job_experience: Any,
    job_education: Any,
) -> float:
    experience_matched, _ = compare_term_sets(job_experience, resume_experience)
    education_matched, _ = compare_term_sets(job_education, resume_education)

    experience_ratio = coverage_ratio(job_experience, experience_matched)
    education_ratio = coverage_ratio(job_education, education_matched)

    if _normalize_terms(job_experience) and _normalize_terms(job_education):
        return (experience_ratio + education_ratio) / 2.0

    if _normalize_terms(job_experience):
        return experience_ratio

    if _normalize_terms(job_education):
        return education_ratio

    return 1.0


def _calculate_match_score(
    semantic_similarity: float,
    skill_coverage: float,
    keyword_coverage: float,
    experience_relevance: float,
    semantic_weight: float,
    skill_weight: float,
    keyword_weight: float,
    experience_weight: float,
) -> int:
    raw_score = (
        semantic_similarity * semantic_weight
        + skill_coverage * skill_weight
        + keyword_coverage * keyword_weight
        + experience_relevance * experience_weight
    )
    return int(max(0, min(100, round(raw_score * 100))))


def _normalize_terms(value: Any) -> list[str]:
    if isinstance(value, str):
        value = value.strip().lower()
        return [value] if value else []
    if isinstance(value, list):
        return [item.strip().lower() for item in value if isinstance(item, str) and item.strip()]
    return []
