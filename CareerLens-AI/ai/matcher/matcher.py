"""Semantic resume-job matching engine for CareerLens AI.

This module computes semantic similarity between a resume profile and a job
profile using sentence transformers embeddings, cosine similarity, and keyword
coverage. It is designed to keep the public API stable while allowing the
underlying embedding model to be replaced in the future.
"""

from __future__ import annotations

import logging
import re
from functools import lru_cache
from typing import Any, Protocol

import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"
DEFAULT_SEMANTIC_WEIGHT = 0.7
DEFAULT_SKILL_WEIGHT = 0.2
DEFAULT_KEYWORD_WEIGHT = 0.1
DEFAULT_FUZZY_THRESHOLD = 85

try:
    from rapidfuzz import fuzz

    _RAPIDFUZZ_AVAILABLE = True
except ImportError:  # pragma: no cover
    fuzz = None  # type: ignore[assignment]
    _RAPIDFUZZ_AVAILABLE = False


class MatchingConfig(Protocol):
    """Configuration for the matcher engine."""

    model_name: str
    semantic_weight: float
    skill_weight: float
    keyword_weight: float
    fuzzy_match_threshold: int


class MatchResult(Protocol):
    """Structured result returned by the resume-job matcher."""

    match_score: int
    semantic_similarity: float
    matched_skills: list[str]
    missing_skills: list[str]
    matched_keywords: list[str]
    missing_keywords: list[str]


class EmbeddingProvider(Protocol):
    """Embedding provider abstraction for easy replacement."""

    def encode(self, texts: list[str]) -> np.ndarray:
        ...


class _SentenceTransformerEmbeddingProvider:
    """Sentence Transformers embedding provider with lazy model loading."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self._model: SentenceTransformer | None = None

    def encode(self, texts: list[str]) -> np.ndarray:
        if self._model is None:
            logger.debug("Loading sentence-transformers model '%s'", self.model_name)
            self._model = SentenceTransformer(self.model_name)
        return np.asarray(self._model.encode(texts, convert_to_numpy=True))


def match_resume_to_job(
    resume_profile: dict[str, Any],
    job_profile: dict[str, Any],
    config: dict[str, Any] | None = None,
    embedding_provider: EmbeddingProvider | None = None,
) -> dict[str, Any]:
    """Match a resume profile against a job profile and return match metrics."""
    if not isinstance(resume_profile, dict) or not isinstance(job_profile, dict):
        logger.warning("Matcher received invalid profile input.")
        return _empty_match_result()

    effective_config = _build_config(config)
    provider = embedding_provider or _get_embedding_provider(effective_config["model_name"])

    resume_text = _build_resume_text(resume_profile)
    job_text = _build_job_text(job_profile)

    try:
        embeddings = provider.encode([resume_text, job_text])
        semantic_similarity = float(_cosine_similarity(embeddings[0], embeddings[1]))
    except Exception as error:  # pragma: no cover
        logger.exception("Failed to compute semantic similarity.")
        semantic_similarity = 0.0

    matched_skills, missing_skills = _compare_skills(
        resume_profile.get("skills"), job_profile.get("required_skills"), effective_config
    )
    matched_keywords, missing_keywords = _compare_keywords(
        resume_text, job_profile.get("keywords"), effective_config
    )

    skill_coverage = _coverage_ratio(matched_skills, job_profile.get("required_skills"))
    keyword_coverage = _coverage_ratio(matched_keywords, job_profile.get("keywords"))

    match_score = _calculate_match_score(
        semantic_similarity=semantic_similarity,
        skill_coverage=skill_coverage,
        keyword_coverage=keyword_coverage,
        config=effective_config,
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


def _build_config(config: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "model_name": str(config.get("model_name", DEFAULT_MODEL_NAME))
        if isinstance(config, dict)
        else DEFAULT_MODEL_NAME,
        "semantic_weight": float(config.get("semantic_weight", DEFAULT_SEMANTIC_WEIGHT))
        if isinstance(config, dict)
        else DEFAULT_SEMANTIC_WEIGHT,
        "skill_weight": float(config.get("skill_weight", DEFAULT_SKILL_WEIGHT))
        if isinstance(config, dict)
        else DEFAULT_SKILL_WEIGHT,
        "keyword_weight": float(config.get("keyword_weight", DEFAULT_KEYWORD_WEIGHT))
        if isinstance(config, dict)
        else DEFAULT_KEYWORD_WEIGHT,
        "fuzzy_match_threshold": int(config.get("fuzzy_match_threshold", DEFAULT_FUZZY_THRESHOLD))
        if isinstance(config, dict)
        else DEFAULT_FUZZY_THRESHOLD,
    }


@lru_cache(maxsize=4)
def _get_embedding_provider(model_name: str) -> EmbeddingProvider:
    return _SentenceTransformerEmbeddingProvider(model_name)


def _build_resume_text(resume_profile: dict[str, Any]) -> str:
    return " ".join(
        _normalize_string(value)
        for key, value in resume_profile.items()
        if key in {
            "skills",
            "education",
            "experience",
            "projects",
            "certifications",
            "languages",
        }
        for value in ([value] if isinstance(value, str) else value if isinstance(value, list) else [])
    )


def _build_job_text(job_profile: dict[str, Any]) -> str:
    return " ".join(
        _normalize_string(value)
        for key, value in job_profile.items()
        if key in {
            "job_title",
            "required_skills",
            "experience_required",
            "education_required",
            "keywords",
        }
        for value in ([value] if isinstance(value, str) else value if isinstance(value, list) else [])
    )


def _normalize_string(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return " ".join(str(item).strip() for item in value if isinstance(item, str))
    return ""


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    if a.size == 0 or b.size == 0:
        return 0.0

    dot_product = float(np.dot(a, b))
    magnitude = float(np.linalg.norm(a) * np.linalg.norm(b))
    if magnitude <= 0:
        return 0.0
    return max(0.0, min(1.0, dot_product / magnitude))


def _compare_skills(
    resume_skills: Any, required_skills: Any, config: dict[str, Any]
) -> tuple[list[str], list[str]]:
    resume_skills_list = _normalize_terms(resume_skills)
    required_skills_list = _normalize_terms(required_skills)

    matched: list[str] = []
    missing: list[str] = []

    for required in required_skills_list:
        if _skill_matches(required, resume_skills_list, config):
            matched.append(required)
        else:
            missing.append(required)

    return matched, missing


def _compare_keywords(
    resume_text: str, job_keywords: Any, config: dict[str, Any]
) -> tuple[list[str], list[str]]:
    normalized_keywords = _normalize_terms(job_keywords)
    matched: list[str] = []
    missing: list[str] = []

    for keyword in normalized_keywords:
        if _keyword_present(keyword, resume_text, config):
            matched.append(keyword)
        else:
            missing.append(keyword)

    return matched, missing


def _normalize_terms(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value.strip().lower()] if value.strip() else []
    if isinstance(value, list):
        return [str(item).strip().lower() for item in value if isinstance(item, str) and str(item).strip()]
    return []


def _skill_matches(skill: str, resume_skills: list[str], config: dict[str, Any]) -> bool:
    if skill in resume_skills:
        return True

    for resume_skill in resume_skills:
        if skill in resume_skill or resume_skill in skill:
            return True

    if _RAPIDFUZZ_AVAILABLE:
        return any(
            fuzz.partial_ratio(skill, resume_skill) >= config["fuzzy_match_threshold"]
            for resume_skill in resume_skills
        )

    return False


def _keyword_present(keyword: str, resume_text: str, config: dict[str, Any]) -> bool:
    needle = keyword.lower().strip()
    haystack = resume_text.lower()
    if needle in haystack:
        return True

    if _RAPIDFUZZ_AVAILABLE:
        return fuzz.partial_ratio(needle, haystack) >= config["fuzzy_match_threshold"]

    return False


def _coverage_ratio(matched: list[str], required: Any) -> float:
    required_list = _normalize_terms(required)
    if not required_list:
        return 1.0
    return len(matched) / len(required_list)


def _calculate_match_score(
    semantic_similarity: float,
    skill_coverage: float,
    keyword_coverage: float,
    config: dict[str, Any],
) -> int:
    raw_score = (
        semantic_similarity * config["semantic_weight"]
        + skill_coverage * config["skill_weight"]
        + keyword_coverage * config["keyword_weight"]
    )
    return int(max(0, min(100, round(raw_score * 100))))
