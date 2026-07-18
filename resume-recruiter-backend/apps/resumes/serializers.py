from rest_framework import serializers

from .models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ("id", "filename", "file_type", "processing_status", "created_at")
        read_only_fields = ("id", "created_at", "processing_status")


class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ("file",)

    def validate_file(self, value):
        allowed_types = {
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }
        extension = value.name.rsplit(".", 1)[-1].lower() if "." in value.name else ""
        if value.content_type not in allowed_types or extension not in {"pdf", "docx"}:
            raise serializers.ValidationError("Only PDF and DOCX files are supported")
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File too large. Maximum size is 10MB")
        return value
