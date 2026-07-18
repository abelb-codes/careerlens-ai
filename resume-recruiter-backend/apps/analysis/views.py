from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.resumes.models import Resume

from .models import Analysis
from .serializers import AnalysisSerializer


class AnalysisDetailView(generics.RetrieveAPIView):
    serializer_class = AnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Analysis.objects.filter(resume__owner=self.request.user)

    def get_object(self):
        resume_id = self.kwargs.get("resume_id")
        return self.get_queryset().get(resume__id=resume_id)


class AnalysisTriggerView(APIView):
    """
    POST /api/analysis/<resume_id>/trigger/

    Re-triggers AI analysis for an existing resume.
    Returns 202 Accepted immediately; analysis runs asynchronously.
    Returns 404 if the resume does not belong to the authenticated user.
    Returns 409 Conflict if the resume is already being processed.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, resume_id, *args, **kwargs):
        try:
            resume = Resume.objects.get(id=resume_id, owner=request.user)
        except Resume.DoesNotExist:
            return Response({"detail": "Resume not found."}, status=status.HTTP_404_NOT_FOUND)

        if resume.processing_status == Resume.ProcessingStatus.PROCESSING:
            return Response(
                {"detail": "Resume is already being processed."},
                status=status.HTTP_409_CONFLICT,
            )

        # Import here to avoid circular imports at module load time
        from apps.analysis.tasks import analyze_resume_task

        resume.processing_status = Resume.ProcessingStatus.UPLOADED
        resume.save(update_fields=["processing_status", "updated_at"])
        analyze_resume_task.delay(str(resume.id))

        return Response(
            {"detail": "Analysis triggered.", "resume_id": str(resume.id)},
            status=status.HTTP_202_ACCEPTED,
        )
