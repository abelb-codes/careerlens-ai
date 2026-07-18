from django.urls import path

from .views import AnalysisDetailView, AnalysisTriggerView

urlpatterns = [
    path("<uuid:resume_id>/", AnalysisDetailView.as_view(), name="analysis-detail"),
    path("<uuid:resume_id>/trigger/", AnalysisTriggerView.as_view(), name="analysis-trigger"),
]
