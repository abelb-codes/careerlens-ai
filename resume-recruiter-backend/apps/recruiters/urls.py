from django.urls import path

from .views import JobListCreateView, JobUploadResumesView, RankingView

urlpatterns = [
    path("", JobListCreateView.as_view(), name="job-list"),
    path("<uuid:pk>/upload-resumes/", JobUploadResumesView.as_view(), name="job-upload-resumes"),
    path("<uuid:pk>/ranking/", RankingView.as_view(), name="job-ranking"),
]
