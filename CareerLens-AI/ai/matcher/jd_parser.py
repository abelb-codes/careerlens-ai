"""Job description parsing utilities for CareerLens AI.

This module converts raw job description text into a structured job profile.
It is intentionally lightweight and rule-based so the architecture can later
replace the parser with model-backed NLP without changing the contract.
"""

from __future__ import annotations

import logging
import re
import string
from collections import Counter
from typing import Any, TypedDict

logger = logging.getLogger(__name__)

SKILL_KEYWORDS = [
    "python",
    "django",
    "flask",
    "fastapi",
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "rest api",
    "graphql",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "javascript",
    "react",
    "angular",
    "vue",
    "html",
    "css",
    "tensorflow",
    "pytorch",
    "nlp",
    "machine learning",
    "data engineering",
    "ci/cd",
    "devops",
]

DEGREE_KEYWORDS = [
    "bachelor",
    "master",
    "mba",
    "phd",
    "associate",
    "high school",
    "diploma",
]

EXPERIENCE_PATTERNS = [
    re.compile(r"(\d+)\+?\s*years?\s+of\s+experience", re.IGNORECASE),
    re.compile(r"(\d+)\+?\s*years?\s+experience", re.IGNORECASE),
    re.compile(r"(\d+)-(\d+)\s+years?\s+experience", re.IGNORECASE),
    re.compile(r"\b(senior|junior|mid[- ]level|lead|principal|entry[- ]level)\b", re.IGNORECASE),
]

JOB_TITLE_PATTERNS = [
    re.compile(r"^\s*(?:Job\s+Title|Position|Role)\s*[:\-]\s*(.+)$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\s*Hiring\s+for\s+(.+)$", re.IGNORECASE),
]

STOPWORDS = {
    "and",
    "or",
    "with",
    "the",
    "a",
    "an",
    "to",
    "for",
    "of",
    "in",
    "on",
    "is",
    "are",
    "by",
    "as",
    "that",
    "this",
    "will",
    "must",
    "required",
    "experience",
    "minimum",
    "years",
    "strong",
    "team",
    "work",
    "including",
    "ability",
    "good",
    "knowledge",
    "preferred",
    "business",
}


class JobDescriptionProfile(TypedDict):
    """Structured representation of a parsed job description."""

    job_title: str
    required_skills: list[str]
    experience_required: list[str]
    education_required: list[str]
    keywords: list[str]


def parse_job_description(raw_text: str) -> JobDescriptionProfile:
    """Parse raw job description text into a structured job profile."""
    if not isinstance(raw_text, str):
        logger.warning("Job description parser received non-string input.")
        return _empty_job_description()

    text = raw_text.strip()
    if not text:
        logger.warning("Job description parser received empty text.")
        return _empty_job_description()

    normalized_text = _normalize_text(text)
    job_title = _extract_job_title(normalized_text)
    required_skills = _extract_required_skills(normalized_text)
    experience_required = _extract_experience_requirements(normalized_text)
    education_required = _extract_education_requirements(normalized_text)
    keywords = _extract_keywords(
        normalized_text,
        exclusions={job_title.lower()} | set(required_skills) | set(experience_required) | set(education_required),
    )

    return {
        "job_title": job_title,
        "required_skills": required_skills,
        "experience_required": experience_required,
        "education_required": education_required,
        "keywords": keywords,
    }


def _empty_job_description() -> JobDescriptionProfile:
    return {
        "job_title": "",
        "required_skills": [],
        "experience_required": [],
        "education_required": [],
        "keywords": [],
    }


def _normalize_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def _extract_job_title(text: str) -> str:
    for pattern in JOB_TITLE_PATTERNS:
        match = pattern.search(text)
        if match:
            title = match.group(1).strip()
            logger.debug("Extracted job title from labeled section: %s", title)
            return title

    first_line = text.splitlines()[0].strip()
    if first_line:
        title_candidate = re.sub(r"^[\u2022\-\*\s]+", "", first_line)
        logger.debug("Using first line as fallback job title: %s", title_candidate)
        return title_candidate

    logger.debug("No explicit job title found; returning empty title.")
    return ""


def _extract_required_skills(text: str) -> list[str]:
    found_skills: list[str] = []
    lowercase_text = text.lower()

    for skill in SKILL_KEYWORDS:
        pattern = re.compile(r"\b" + re.escape(skill) + r"\b", re.IGNORECASE)
        if pattern.search(lowercase_text):
            normalized_skill = skill.lower()
            if normalized_skill not in found_skills:
                found_skills.append(normalized_skill)

    return found_skills


def _extract_experience_requirements(text: str) -> list[str]:
    experience_items: list[str] = []
    for pattern in EXPERIENCE_PATTERNS:
        for match in pattern.finditer(text):
            experience_phrase = match.group(0).strip().lower()
            if experience_phrase not in experience_items:
                experience_items.append(experience_phrase)

    return experience_items


def _extract_education_requirements(text: str) -> list[str]:
    education_items: list[str] = []
    for degree in DEGREE_KEYWORDS:
        pattern = re.compile(r"\b" + re.escape(degree) + r"\b", re.IGNORECASE)
        if pattern.search(text):
            normalized_degree = degree.lower()
            if normalized_degree not in education_items:
                education_items.append(normalized_degree)

    return education_items


def _extract_keywords(text: str, exclusions: set[str]) -> list[str]:
    cleaned = text.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    tokens = [token.lower() for token in cleaned.split() if token]
    tokens = [token for token in tokens if token not in STOPWORDS and token.isalpha()]
    tokens = [token for token in tokens if token not in exclusions]

    counts = Counter(tokens)
    most_common = [token for token, _ in counts.most_common(10)]
    logger.debug("Extracted keywords: %s", most_common)
    return most_common
