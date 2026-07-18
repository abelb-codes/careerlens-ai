import logging

from apps.analysis.models import Analysis
from apps.resumes.models import Resume

from .client import AIServiceClient, AIServiceError

logger = logging.getLogger(__name__)


class AIAnalysisService:
    def __init__(self, client=None):
        self.client = client or AIServiceClient()

    def _normalize_analysis_payload(self, result: dict) -> dict:
        matching_result = result.get("matching_result") or {}
        return {
            "ats_score": result.get("ats_score", result.get("resume_score", 0)),
            "quality_score": result.get("quality_score", result.get("resume_score", 0)),
            "matching_score": result.get("matching_score", matching_result.get("matching_score", matching_result.get("score", 0))),
            "extracted_skills": result.get("skills") or result.get("extracted_skills", []),
            "extracted_experience": result.get("experience") or result.get("extracted_experience", []),
            "extracted_education": result.get("education") or result.get("extracted_education", []),
            "suggestions": result.get("suggestions") or result.get("recommendations", []),
            "interview_questions": result.get("interview_questions", []),
        }

    def run_analysis(self, resume: Resume) -> Analysis:
        """
        Runs AI analysis for a resume and stores the result.
        Marks resume as 'failed' if the AI Engine call fails.

        Returns the Analysis object on success.
        Raises AIServiceError on failure (caller should also mark resume failed).
        """
        try:
            result = self.client.analyze_document(resume.file.path, resume.filename)
        except AIServiceError as exc:
            logger.error(
                "AI analysis failed for resume %s (%s): %s",
                resume.id,
                resume.filename,
                exc,
            )
            resume.processing_status = Resume.ProcessingStatus.FAILED
            resume.save(update_fields=["processing_status", "updated_at"])
            raise

        normalized = self._normalize_analysis_payload(result)
        analysis, _ = Analysis.objects.update_or_create(
            resume=resume,
            defaults={
                "ats_score": normalized["ats_score"],
                "quality_score": normalized["quality_score"],
                "matching_score": normalized["matching_score"],
                "extracted_skills": normalized["extracted_skills"],
                "extracted_experience": normalized["extracted_experience"],
                "extracted_education": normalized["extracted_education"],
                "suggestions": normalized["suggestions"],
                "interview_questions": normalized["interview_questions"],
            },
        )
        resume.processing_status = Resume.ProcessingStatus.COMPLETED
        resume.save(update_fields=["processing_status", "updated_at"])
        logger.info("AI analysis completed for resume %s (%s)", resume.id, resume.filename)
        return analysis
