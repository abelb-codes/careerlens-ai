from django.urls import path

from .views import ResumeDetailView, ResumeListCreateView

urlpatterns = [
    path("upload/", ResumeListCreateView.as_view(), name="resume-upload"),
    path("", ResumeListCreateView.as_view(), name="resume-list"),
    path("<uuid:pk>/", ResumeDetailView.as_view(), name="resume-detail"),
]
