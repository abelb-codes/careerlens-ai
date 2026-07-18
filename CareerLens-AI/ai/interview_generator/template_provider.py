"""Template-based interview question provider for CareerLens AI.

This provider generates candidate-specific interview questions using resume,
job, and matching context. It is intentionally template-driven so it can be
replaced later by cloud or local LLM providers without changing the public
interview generation API.
"""

from __future__ import annotations

import logging
from typing import Any

from ai.interview_generator.base_provider import InterviewProvider

logger = logging.getLogger(__name__)


class TemplateInterviewProvider(InterviewProvider):
    """Interview question provider that uses template logic."""

    def generate_questions(
        self,
        resume_profile: dict[str, Any] | None,
        job_profile: dict[str, Any] | None,
        matching_result: dict[str, Any] | None,
    ) -> dict[str, list[str]]:
        """Generate exactly five personalized interview questions."""
        resume = _normalize_profile(resume_profile)
        job = _normalize_profile(job_profile)
        matching = _normalize_profile(matching_result)

        skills = _extract_list(resume.get("skills"))
        projects = _extract_list(resume.get("projects"))
        experience = _extract_list(resume.get("experience"))
        missing_skills = _extract_list(matching.get("missing_skills"))
        required_skills = _extract_list(job.get("required_skills"))
        keywords = _extract_list(job.get("keywords"))

        skill_target = _first_nonempty(
            skills,
            matching.get("matched_skills"),
            required_skills,
            keywords,
            ["technical skills"],
        )
        project_topic = _first_nonempty(projects, skills, keywords, ["a recent project"])
        experience_topic = _first_nonempty(experience, skills, required_skills, ["your work history"])
        missing_skill = _first_nonempty(missing_skills, required_skills, ["a required skill for this role"])
        role_name = str(job.get("job_title") or "the role").strip() or "the role"

        questions = [
            _build_technical_question(skill_target, role_name),
            _build_project_question(project_topic, skill_target, role_name),
            _build_experience_question(experience_topic, skill_target, role_name),
            _build_missing_skill_question(missing_skill, role_name),
            _build_job_focus_question(role_name, required_skills, keywords),
        ]

        questions = _ensure_exactly_five_questions(questions, resume, job, matching)

        return {"questions": questions}


def _normalize_profile(profile: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(profile, dict):
        return {}
    return profile


def _extract_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if isinstance(item, str) and item.strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def _first_nonempty(*sources: Any) -> list[str] | str:
    for source in sources:
        if isinstance(source, list) and source:
            return source
        if isinstance(source, str) and source.strip():
            return source.strip()
    return []


def _build_technical_question(skill_target: list[str] | str, role_name: str) -> str:
    skill_str = _render_item(skill_target, fallback="your main technical skill")
    return (
        f"For {role_name}, how would you apply {skill_str} to solve a complex problem in this domain?"
    )


def _build_project_question(project_topic: list[str] | str, skill_target: list[str] | str, role_name: str) -> str:
    project_str = _render_item(project_topic, fallback="a relevant project")
    skill_str = _render_item(skill_target, fallback="a key technology")
    return (
        f"In {project_str}, what was the hardest technical decision you made, and how did it prepare you for a {role_name}?"
    )


def _build_experience_question(experience_topic: list[str] | str, skill_target: list[str] | str, role_name: str) -> str:
    experience_str = _render_item(experience_topic, fallback="an experience from your background")
    skill_str = _render_item(skill_target, fallback="the role's main technical challenge")
    return (
        f"Describe a time during {experience_str} when you solved a problem using {skill_str} for a {role_name}."
    )


def _build_missing_skill_question(missing_skill: list[str] | str, role_name: str) -> str:
    missing_str = _render_item(missing_skill, fallback="an important skill for this role")
    return (
        f"This position calls for {missing_str}. How would you close that gap or demonstrate related ability during an interview?"
    )


def _build_job_focus_question(role_name: str, required_skills: list[str], keywords: list[str]) -> str:
    focus = _render_item(required_skills, fallback=keywords, joiner=" or ", fallback_text="a core requirement")
    return (
        f"As a candidate for {role_name}, how would you approach a problem that requires {focus} while balancing speed and quality?"
    )


def _render_item(
    item: list[str] | str | None,
    fallback: list[str] | str | None = None,
    joiner: str = ", ",
    fallback_text: str = "a relevant topic",
) -> str:
    if isinstance(item, list) and item:
        if len(item) == 1:
            return item[0]
        return joiner.join(item[:2])
    if isinstance(item, str) and item:
        return item
    if isinstance(fallback, list) and fallback:
        if len(fallback) == 1:
            return fallback[0]
        return joiner.join(fallback[:2])
    if isinstance(fallback, str) and fallback:
        return fallback
    return fallback_text


def _ensure_exactly_five_questions(
    questions: list[str],
    resume: dict[str, Any],
    job: dict[str, Any],
    matching: dict[str, Any],
) -> list[str]:
    unique_questions = []
    seen = set()

    for question in questions:
        normalized = question.strip()
        if normalized and normalized not in seen:
            unique_questions.append(normalized)
            seen.add(normalized)

    while len(unique_questions) < 5:
        fallback = _build_fallback_question(resume, job, matching, len(unique_questions))
        if fallback not in seen:
            unique_questions.append(fallback)
            seen.add(fallback)
        else:
            unique_questions.append(f"Tell me more about your career goals for this role.")
            seen.add(unique_questions[-1])

    return unique_questions[:5]


def _build_fallback_question(
    resume: dict[str, Any], job: dict[str, Any], matching: dict[str, Any], position: int
) -> str:
    job_title = str(job.get("job_title") or "the role").strip() or "the role"
    if position == 0:
        return f"What draws you to {job_title}, and how does your background support success in this position?"
    if position == 1:
        top_skill = _render_item(_extract_list(resume.get("skills")), fallback=job.get("required_skills"), fallback_text="relevant skills")
        return f"Which {top_skill} have you found most valuable, and why?"
    if position == 2:
        top_project = _render_item(_extract_list(resume.get("projects")), fallback_text="a recent project")
        return f"What was the biggest challenge in {top_project}, and how did you overcome it?"
    if position == 3:
        missing = _render_item(_extract_list(matching.get("missing_skills")), fallback=job.get("required_skills"), fallback_text="a role requirement")
        return f"How would you ramp up on {missing} if selected for this {job_title}?"
    return f"How do you prioritize learning new tools or skills when preparing for a new position?"
