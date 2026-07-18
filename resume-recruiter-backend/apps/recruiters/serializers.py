from rest_framework import serializers

from .models import CandidateMatch, JobDescription


class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = ("id", "title", "description", "required_skills", "created_at")
        read_only_fields = ("id", "created_at")


class CandidateMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateMatch
        fields = ("id", "resume", "similarity_score", "ranking_position", "created_at")
        read_only_fields = fields
