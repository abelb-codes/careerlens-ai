import uuid

from django.conf import settings
from django.db import models

from apps.resumes.models import Resume


class JobDescription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "job_descriptions"
        indexes = [models.Index(fields=["recruiter", "created_at"], name="idx_jobs_recruiter_created")]

    def __str__(self) -> str:
        return self.title


class CandidateMatch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE, related_name="matches")
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="matches")
    similarity_score = models.FloatField(default=0.0)
    ranking_position = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "candidate_matches"
        indexes = [models.Index(fields=["job", "ranking_position"], name="idx_matches_job_rank")]
