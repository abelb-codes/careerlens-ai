import logging

from celery import shared_task

from apps.ai_service.client import AIServiceError
from apps.ai_service.services import AIAnalysisService
from apps.resumes.models import Resume

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def analyze_resume_task(self, resume_id: str):
    """
    Celery task to run AI analysis for a resume.

    Marks the resume as 'processing' before starting, 'completed' on success,
    and 'failed' on error. Retries up to 2 times on transient AI service failures.
    """
    try:
        resume = Resume.objects.get(id=resume_id)
    except Resume.DoesNotExist:
        logger.error("analyze_resume_task: Resume %s not found — skipping.", resume_id)
        return

    resume.processing_status = Resume.ProcessingStatus.PROCESSING
    resume.save(update_fields=["processing_status", "updated_at"])
    logger.info("Starting AI analysis for resume %s (%s)", resume_id, resume.filename)

    try:
        AIAnalysisService().run_analysis(resume)
        logger.info("AI analysis completed for resume %s", resume_id)
    except AIServiceError as exc:
        logger.warning(
            "AI service error for resume %s (attempt %d/%d): %s",
            resume_id,
            self.request.retries + 1,
            self.max_retries + 1,
            exc,
        )
        # Retry on transient failures; give up and mark failed after max_retries
        try:
            raise self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            logger.error("Max retries exceeded for resume %s — marking failed.", resume_id)
            resume.processing_status = Resume.ProcessingStatus.FAILED
            resume.save(update_fields=["processing_status", "updated_at"])
    except Exception as exc:
        logger.exception("Unexpected error analyzing resume %s: %s", resume_id, exc)
        resume.processing_status = Resume.ProcessingStatus.FAILED
        resume.save(update_fields=["processing_status", "updated_at"])
        raise
