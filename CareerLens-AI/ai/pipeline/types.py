"""Pipeline contract types for CareerLens AI orchestration."""

from __future__ import annotations

from typing import Any, TypedDict


class ApplicantPipelineInput(TypedDict, total=False):
    """Input data required to process a single applicant."""

    resume_file_path: str
    job_profile: dict[str, Any]
    ranking_config: dict[str, Any]
    matcher_config: dict[str, Any]
    interview_provider: Any


class RecruiterPipelineInput(TypedDict, total=False):
    """Input data required to process recruiter requests."""

    job_profile: dict[str, Any]
    candidate_resume_file_paths: list[str]
    ranking_config: dict[str, Any]
    matcher_config: dict[str, Any]
    interview_provider: Any


class ApplicantPipelineOutput(TypedDict, total=False):
    """Structured output returned by the applicant pipeline."""

    candidate_report: dict[str, Any]
    resume_profile: dict[str, Any]
    resume_analysis: dict[str, Any]
    matching_result: dict[str, Any]
    interview_questions: list[str]
    error: str


class RecruiterPipelineOutput(TypedDict, total=False):
    """Structured output returned by the recruiter pipeline."""

    candidate_reports: list[dict[str, Any]]
    ranked_candidates: list[dict[str, Any]]
    job_profile: dict[str, Any]
    error: str


class PipelineConfig(TypedDict, total=False):
    """Configuration object for orchestration pipelines."""

    ranking_config: dict[str, Any]
    matcher_config: dict[str, Any]
    interview_provider: Any
