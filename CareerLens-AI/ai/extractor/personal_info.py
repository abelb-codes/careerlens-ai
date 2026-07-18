# ai/extractor/personal_info.py
"""
Personal information extraction utilities for resume text.

This module extracts candidate name, email address, and phone number from
plain text produced by the parser layer.
"""

from __future__ import annotations

import logging
import re
from typing import TypedDict

logger = logging.getLogger(__name__)

EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_REGEX = re.compile(
    r"""
    (?:
        (?:\+?\d{1,3}[\s.-]?)?
        (?:\(?\d{2,4}\)?[\s.-]?)?
        \d{3,4}[\s.-]?\d{3,4}
    )
    """,
    re.VERBOSE,
)

LINK_HINTS = ("http", "www.", "linkedin", "github.com", "portfolio")
SECTION_KEYWORDS = {
    "address",
    "certifications",
    "contact",
    "curriculum",
    "education",
    "email",
    "experience",
    "languages",
    "mobile",
    "objective",
    "phone",
    "portfolio",
    "profile",
    "projects",
    "resume",
    "skills",
    "summary",
    "vitae",
}
TITLE_KEYWORDS = {
    "administrator",
    "analyst",
    "architect",
    "consultant",
    "coordinator",
    "designer",
    "developer",
    "director",
    "engineer",
    "executive",
    "intern",
    "lead",
    "manager",
    "officer",
    "specialist",
}


class PersonalInfo(TypedDict):
    """Structured personal details extracted from resume text."""

    name: str
    email: str
    phone: str


def extract_personal_info(text: str) -> PersonalInfo:
    """
    Extract candidate name, email address, and phone number from resume text.

    Parameters
    ----------
    text:
        Plain resume text returned by the parser module.

    Returns
    -------
    PersonalInfo
        A dictionary containing ``name``, ``email``, and ``phone`` keys.
        Missing values are returned as empty strings.
    """
    if not isinstance(text, str):
        logger.warning("Personal information extraction received non-string input.")
        return _empty_personal_info()

    email = _extract_email(text)
    phone = _extract_phone(text)
    name = _extract_name(text, email=email, phone=phone)

    return {
        "name": name,
        "email": email,
        "phone": phone,
    }


def _empty_personal_info() -> PersonalInfo:
    """Return an empty result that preserves the personal information schema."""
    return {
        "name": "",
        "email": "",
        "phone": "",
    }


def _extract_email(text: str) -> str:
    """Return the first email address found in the text."""
    match = EMAIL_REGEX.search(text)
    return match.group(0).lower() if match else ""


def _extract_phone(text: str) -> str:
    """Return the first plausible phone number found in the text."""
    for match in PHONE_REGEX.finditer(text):
        phone = match.group(0).strip()
        digit_count = len(re.sub(r"\D", "", phone))
        if 7 <= digit_count <= 15:
            return phone
    return ""


def _extract_name(text: str, email: str, phone: str) -> str:
    """Infer the candidate name from the first meaningful resume lines."""
    lines = _non_empty_lines(text)
    contact_fragments = _contact_fragments(email=email, phone=phone)

    for line in lines[:10]:
        if _is_name_candidate(line, contact_fragments):
            return line

    return ""


def _non_empty_lines(text: str) -> list[str]:
    """Split text into stripped, non-empty lines."""
    return [line.strip() for line in text.splitlines() if line.strip()]


def _contact_fragments(email: str, phone: str) -> set[str]:
    """Build lowercase fragments that should not be mistaken for a name."""
    fragments: set[str] = set()

    if email:
        fragments.add(email.lower())

    if phone:
        fragments.add(phone.lower())
        digits_only = re.sub(r"\D", "", phone)
        if digits_only:
            fragments.add(digits_only)

    return fragments


def _is_name_candidate(line: str, contact_fragments: set[str]) -> bool:
    """Return True when a line looks like a human name."""
    normalized_line = line.lower()

    if any(fragment and fragment in normalized_line for fragment in contact_fragments):
        return False

    if any(hint in normalized_line for hint in LINK_HINTS):
        return False

    words = line.split()
    if not 2 <= len(words) <= 4:
        return False

    cleaned_words = [_clean_name_word(word) for word in words]
    if any(not word for word in cleaned_words):
        return False

    lowered_words = {word.lower() for word in cleaned_words}
    if lowered_words & SECTION_KEYWORDS:
        return False

    if lowered_words & TITLE_KEYWORDS:
        return False

    return all(_looks_like_name_word(word) for word in cleaned_words)


def _clean_name_word(word: str) -> str:
    """Remove punctuation that commonly appears around name tokens."""
    return word.strip(" ,:;|()[]{}")


def _looks_like_name_word(word: str) -> bool:
    """Return True when a token resembles a name word or initial."""
    if re.fullmatch(r"[A-Z]\.?", word):
        return True

    if re.fullmatch(r"[A-Z][a-zA-Z'-]+", word):
        return True

    return False
