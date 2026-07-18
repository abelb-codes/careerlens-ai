from rest_framework import serializers

from .models import Analysis


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = (
            "id",
            "resume",
            "ats_score",
            "quality_score",
            "matching_score",
            "extracted_skills",
            "extracted_experience",
            "extracted_education",
            "suggestions",
            "interview_questions",
            "created_at",
        )
        read_only_fields = fields
