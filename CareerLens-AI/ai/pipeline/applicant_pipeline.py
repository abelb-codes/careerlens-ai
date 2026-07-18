"""Applicant-level AI orchestration for CareerLens AI."""

from __future__ import annotations

import logging
from typing import Any

from ai.analyzer.analyzer import analyze_resume
from ai.extractor.extractor import extract_resume_data
from ai.interview_generator.interview_generator import generate_interview_questions
from ai.matcher.matcher import match_resume_to_job
from ai.parser.parser import parse_resume
from ai.pipeline.exceptions import InvalidPipelineInputError, PipelineExecutionError
from ai.pipeline.types import ApplicantPipelineOutput, PipelineConfig
from ai.reports.report_builder import generate_report


class ApplicantPipeline:
    """Service layer orchestrating a single applicant report flow."""

    def __init__(
        self,
        parser: Any = parse_resume,
        extractor: Any = extract_resume_data,
        analyzer: Any = analyze_resume,
        matcher: Any = match_resume_to_job,
        interview_generator: Any = generate_interview_questions,
        report_builder: Any = generate_report,
        logger: logging.Logger | None = None,
    ) -> None:
        self.parser = parser
        self.extractor = extractor
        self.analyzer = analyzer
        self.matcher = matcher
        self.interview_generator = interview_generator
        self.report_builder = report_builder
        self.logger = logger or logging.getLogger(__name__)

    def process_applicant(
        self,
        resume_file_path: str,
        job_profile: dict[str, Any],
        config: PipelineConfig | None = None,
    ) -> ApplicantPipelineOutput:
        """Process a single applicant through the CareerLens AI pipeline."""
        if not isinstance(resume_file_path, str) or not resume_file_path.strip():
            raise InvalidPipelineInputError("resume_file_path must be a non-empty string")

        if not isinstance(job_profile, dict):
            raise InvalidPipelineInputError("job_profile must be a dictionary")

        pipeline_config = config or {}
        matcher_config = pipeline_config.get("matcher_config")
        interview_provider = pipeline_config.get("interview_provider")

        self.logger.info("Starting applicant pipeline for resume: %s", resume_file_path)

        try:
            parse_result = self.parser(resume_file_path)
            self.logger.debug("Parsed resume result: %s", parse_result)

            extracted_resume = self.extractor(parse_result.get("text", ""))
            self.logger.debug("Extracted resume profile: %s", {"keys": list(extracted_resume.keys())})

            resume_analysis = self.analyzer(extracted_resume)
            self.logger.debug("Resume analysis result: %s", resume_analysis)

            matching_result = self.matcher(
                extracted_resume,
                job_profile,
                config=matcher_config,
            )
            self.logger.debug("Matching result: %s", matching_result)

            interview_result = self.interview_generator(
                extracted_resume,
                job_profile,
                matching_result,
                provider=interview_provider,
            )
            self.logger.debug("Interview questions generated")

            candidate_report = self.report_builder(
                extracted_resume,
                resume_analysis,
                job_profile,
                matching_result,
                {},
                interview_result.get("questions") if isinstance(interview_result, dict) else None,
            )

            error_message = None
            if isinstance(parse_result, dict) and not parse_result.get("success", False):
                error_message = parse_result.get("error") or "Resume parsing failed"
                self.logger.warning(
                    "Applicant pipeline completed with parse warning: %s",
                    error_message,
                )

            return {
                "candidate_report": candidate_report,
                "resume_profile": extracted_resume,
                "resume_analysis": resume_analysis,
                "matching_result": matching_result,
                "interview_questions": interview_result.get("questions")
                if isinstance(interview_result, dict)
                else [],
                "error": error_message or "",
            }
        except InvalidPipelineInputError:
            raise
        except Exception as exc:  # pragma: no cover
            self.logger.exception(
                "Unexpected failure in applicant pipeline for %s",
                resume_file_path,
            )
            raise PipelineExecutionError(
                f"Applicant pipeline failed for {resume_file_path}: {exc}"
            ) from exc
