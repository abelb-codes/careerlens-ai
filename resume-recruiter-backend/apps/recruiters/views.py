from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.resumes.models import Resume

from .models import CandidateMatch, JobDescription
from .serializers import CandidateMatchSerializer, JobDescriptionSerializer


class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobDescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobDescription.objects.filter(recruiter=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)


class JobUploadResumesView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        job = JobDescription.objects.get(id=self.kwargs["pk"], recruiter=request.user)
        resume_ids = request.data.get("resume_ids", [])
        if not isinstance(resume_ids, list):
            return Response({"detail": "resume_ids must be a list"}, status=status.HTTP_400_BAD_REQUEST)

        for index, resume_id in enumerate(resume_ids, start=1):
            resume = Resume.objects.get(id=resume_id, owner=request.user)
            CandidateMatch.objects.update_or_create(
                job=job,
                resume=resume,
                defaults={"similarity_score": 0.0, "ranking_position": index},
            )
        return Response({"detail": "Resumes attached to job"}, status=status.HTTP_201_CREATED)


class RankingView(generics.ListAPIView):
    serializer_class = CandidateMatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CandidateMatch.objects.filter(job__recruiter=self.request.user, job_id=self.kwargs["pk"]).order_by("ranking_position")
