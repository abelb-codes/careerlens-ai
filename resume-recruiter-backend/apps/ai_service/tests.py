from django.test import SimpleTestCase

from apps.ai_service.services import AIAnalysisService


class AIAnalysisServiceTests(SimpleTestCase):
    def test_normalize_analysis_payload_supports_engine_response(self):
        service = AIAnalysisService(client=None)
        payload = {
            "ats_score": 84,
            "resume_score": 91,
            "skills": ["Python", "Django"],
            "experience": [{"role": "Software Engineer"}],
            "education": [{"school": "Example University"}],
            "suggestions": ["Add impact metrics"],
        }

        normalized = service._normalize_analysis_payload(payload)

        self.assertEqual(normalized["ats_score"], 84)
        self.assertEqual(normalized["quality_score"], 91)
        self.assertEqual(normalized["extracted_skills"], ["Python", "Django"])
        self.assertEqual(normalized["extracted_experience"], [{"role": "Software Engineer"}])
        self.assertEqual(normalized["extracted_education"], [{"school": "Example University"}])
        self.assertEqual(normalized["suggestions"], ["Add impact metrics"])
