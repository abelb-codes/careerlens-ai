import uuid

from django.db import models

from apps.resumes.models import Resume


class Analysis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name="analysis")
    ats_score = models.IntegerField(default=0)
    quality_score = models.IntegerField(default=0)
    matching_score = models.IntegerField(default=0)
    extracted_skills = models.JSONField(default=list)
    extracted_experience = models.JSONField(default=list)
    extracted_education = models.JSONField(default=list)
    suggestions = models.JSONField(default=list)
    interview_questions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "analyses"
        indexes = [models.Index(fields=["resume"], name="idx_analyses_resume")]

    def __str__(self) -> str:
        return f"Analysis for {self.resume.filename}"
