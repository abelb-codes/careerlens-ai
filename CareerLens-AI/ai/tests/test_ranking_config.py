"""Unit tests for the ranking configuration module."""

from __future__ import annotations

import unittest

from ai.ranking.config import RankingConfig


class TestRankingConfig(unittest.TestCase):
    """Tests for ranking configuration and normalization."""

    def test_default_weights_normalize_to_one(self) -> None:
        config = RankingConfig()
        weights = config.normalized_weights()

        self.assertAlmostEqual(sum(weights), 1.0)
        self.assertEqual(len(weights), 5)

    def test_from_dict_uses_raw_values(self) -> None:
        config = RankingConfig.from_dict(
            {
                "semantic_weight": 0.6,
                "resume_quality_weight": 0.2,
                "ats_weight": 0.1,
                "experience_weight": 0.05,
                "project_weight": 0.05,
            }
        )

        self.assertAlmostEqual(config.semantic_weight, 0.6)
        self.assertAlmostEqual(config.resume_quality_weight, 0.2)
        self.assertAlmostEqual(config.ats_weight, 0.1)
        self.assertAlmostEqual(config.experience_weight, 0.05)
        self.assertAlmostEqual(config.project_weight, 0.05)

    def test_from_dict_invalid_values_use_defaults(self) -> None:
        config = RankingConfig.from_dict(
            {
                "semantic_weight": "bad",
                "resume_quality_weight": -1,
                "ats_weight": None,
            }
        )

        self.assertAlmostEqual(config.semantic_weight, 0.5)
        self.assertAlmostEqual(config.resume_quality_weight, 0.2)
        self.assertAlmostEqual(config.ats_weight, 0.15)

    def test_normalized_weights_handles_zero_total(self) -> None:
        config = RankingConfig(
            semantic_weight=0,
            resume_quality_weight=0,
            ats_weight=0,
            experience_weight=0,
            project_weight=0,
        )
        weights = config.normalized_weights()

        self.assertAlmostEqual(sum(weights), 1.0)
        self.assertEqual(weights[0], 0.5)


if __name__ == "__main__":
    unittest.main()
