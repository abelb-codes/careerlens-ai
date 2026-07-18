"""Recruiter-facing AI orchestration for CareerLens AI."""

from __future__ import annotations

import logging
from typing import Any

from ai.pipeline.applicant_pipeline import ApplicantPipeline
from ai.pipeline.exceptions import InvalidPipelineInputError, PipelineExecutionError
from ai.pipeline.types import PipelineConfig, RecruiterPipelineOutput
from ai.ranking.ranking_engine import rank_candidates


class RecruiterPipeline:
    """Service layer orchestrating recruiter candidate ranking and reporting."""

    def __init__(
        self,
        applicant_pipeline: ApplicantPipeline | None = None,
        ranking_service: Any = rank_candidates,
        logger: logging.Logger | None = None,
    ) -> None:
        self.applicant_pipeline = applicant_pipeline or ApplicantPipeline()
        self.ranking_service = ranking_service
        self.logger = logger or logging.getLogger(__name__)

    def process_candidates(
        self,
        job_profile: dict[str, Any],
        candidate_resume_file_paths: list[str],
        config: PipelineConfig | None = None,
    ) -> RecruiterPipelineOutput:
        """Process multiple candidates and return ranked recruiter results."""
        if not isinstance(job_profile, dict):
            raise InvalidPipelineInputError("job_profile must be a dictionary")

        if not isinstance(candidate_resume_file_paths, list):
            raise InvalidPipelineInputError("candidate_resume_file_paths must be a list")

        if not candidate_resume_file_paths:
            raise InvalidPipelineInputError("candidate_resume_file_paths must contain at least one resume path")

        pipeline_config = config or {}
        ranking_config = pipeline_config.get("ranking_config")

        self.logger.info(
            "Starting recruiter pipeline for %s candidates.",
            len(candidate_resume_file_paths),
        )

        candidate_reports: list[dict[str, Any]] = []
        pipeline_outputs: list[dict[str, Any]] = []

        for resume_path in candidate_resume_file_paths:
            try:
                output = self.applicant_pipeline.process_applicant(
                    resume_path,
                    job_profile,
                    config=pipeline_config,
                )
                candidate_reports.append(output["candidate_report"])
                pipeline_outputs.append(output)
            except InvalidPipelineInputError:
                raise
            except Exception as error:  # pragma: no cover
                self.logger.exception(
                    "Candidate processing failed for resume: %s",
                    resume_path,
                )
                candidate_reports.append(
                    {
                        "candidate": {},
                        "analysis": {},
                        "job": job_profile,
                        "matching": {},
                        "ranking": {},
                        "interview_questions": [],
                        "generated_at": "",
                        "version": "",
                        "error": str(error),
                    }
                )

        try:
            ranked_candidates = self.ranking_service(
                [
                    {
                        "resume_profile": output["resume_profile"],
                        "analysis": output["resume_analysis"],
                        "matching": output["matching_result"],
                    }
                    for output in pipeline_outputs
                ],
                config=ranking_config,
            )
        except Exception as exc:  # pragma: no cover
            self.logger.exception("Ranking service failed.")
            raise PipelineExecutionError(f"Ranking failed: {exc}") from exc

        return {
            "candidate_reports": candidate_reports,
            "ranked_candidates": ranked_candidates,
            "job_profile": job_profile,
            "error": "",
        }
