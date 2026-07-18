from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.analysis.tasks import analyze_resume_task

from .models import Resume
from .serializers import ResumeSerializer, ResumeUploadSerializer


class ResumeListCreateView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(owner=self.request.user).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        upload_serializer = ResumeUploadSerializer(data=request.data)
        upload_serializer.is_valid(raise_exception=True)
        uploaded_file = upload_serializer.validated_data["file"]
        resume = Resume.objects.create(
            owner=request.user,
            file=uploaded_file,
            filename=uploaded_file.name,
            file_type=uploaded_file.content_type,
        )
        # Schedule only after the upload transaction has committed, otherwise a
        # worker can race the database and fail to find the new resume.
        transaction.on_commit(lambda: analyze_resume_task.delay(str(resume.id)))
        return Response(ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)


class ResumeDetailView(generics.RetrieveAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(owner=self.request.user)
