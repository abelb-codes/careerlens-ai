"""Unit tests for the ranking score calculator."""

from __future__ import annotations

import unittest

from ai.ranking.config import RankingConfig
from ai.ranking.score_calculator import calculate_candidate_score


class TestScoreCalculator(unittest.TestCase):
    """Tests for final candidate score calculation."""

    def test_calculate_candidate_score_uses_all_factors(self) -> None:
        candidate = {
            "analysis": {
                "resume_score": 80,
                "ats_score": 90,
            },
            "matching": {
                "semantic_similarity": 0.9,
                "match_score": 85,
                "experience_relevance": 0.8,
                "project_relevance": 0.7,
            },
        }
        config = RankingConfig()

        score = calculate_candidate_score(candidate, config)

        self.assertGreater(score, 0.0)
        self.assertLessEqual(score, 100.0)

    def test_calculate_candidate_score_invalid_candidate_returns_zero(self) -> None:
        score = calculate_candidate_score(None)  # type: ignore[arg-type]

        self.assertEqual(score, 0.0)

    def test_calculate_candidate_score_missing_fields_uses_defaults(self) -> None:
        candidate = {
            "analysis": {},
            "matching": {},
        }
        score = calculate_candidate_score(candidate, RankingConfig())

        self.assertEqual(score, 0.0)

    def test_calculate_candidate_score_bounds_score_between_zero_and_hundred(self) -> None:
        candidate = {
            "analysis": {
                "resume_score": 200,
                "ats_score": 200,
            },
            "matching": {
                "semantic_similarity": 2.0,
                "match_score": 200,
                "experience_relevance": 2.0,
                "project_relevance": 2.0,
            },
        }
        score = calculate_candidate_score(candidate, RankingConfig())

        self.assertEqual(score, 100.0)


if __name__ == "__main__":
    unittest.main()
