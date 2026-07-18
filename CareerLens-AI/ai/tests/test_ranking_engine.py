"""Unit tests for the ranking engine."""

from __future__ import annotations

import unittest

from ai.ranking.ranking_engine import rank_candidates
from ai.ranking.config import RankingConfig


class TestRankingEngine(unittest.TestCase):
    """Tests for candidate ranking output and ranking stability."""

    def test_rank_candidates_returns_sorted_ranked_list(self) -> None:
        candidates = [
            {
                "name": "Alice",
                "analysis": {"resume_score": 80, "ats_score": 75},
                "matching": {"semantic_similarity": 0.8, "match_score": 82},
            },
            {
                "name": "Bob",
                "analysis": {"resume_score": 90, "ats_score": 85},
                "matching": {"semantic_similarity": 0.7, "match_score": 80},
            },
        ]

        ranked = rank_candidates(candidates)

        self.assertEqual(len(ranked), 2)
        self.assertEqual(ranked[0]["candidate_name"], "Alice")
        self.assertEqual(ranked[1]["candidate_name"], "Bob")
        self.assertEqual(ranked[0]["rank"], 1)
        self.assertEqual(ranked[1]["rank"], 2)

    def test_rank_candidates_handles_invalid_items_and_missing_fields(self) -> None:
        candidates = [
            {
                "name": "Charlie",
                "analysis": {"resume_score": 50},
                "matching": {"semantic_similarity": 0.5, "match_score": 55},
            },
            None,
            "invalid",
        ]

        ranked = rank_candidates(candidates)

        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0]["candidate_name"], "Charlie")
        self.assertEqual(ranked[0]["rank"], 1)
        self.assertGreaterEqual(ranked[0]["final_score"], 0.0)

    def test_rank_candidates_assigns_tied_ranks(self) -> None:
        candidates = [
            {
                "name": "Dave",
                "analysis": {"resume_score": 70, "ats_score": 70},
                "matching": {"semantic_similarity": 0.7, "match_score": 70},
            },
            {
                "name": "Eve",
                "analysis": {"resume_score": 70, "ats_score": 70},
                "matching": {"semantic_similarity": 0.7, "match_score": 70},
            },
        ]

        ranked = rank_candidates(candidates)

        self.assertEqual(len(ranked), 2)
        self.assertEqual(ranked[0]["rank"], 1)
        self.assertEqual(ranked[1]["rank"], 1)
        self.assertEqual(ranked[0]["final_score"], ranked[1]["final_score"])

    def test_rank_candidates_accepts_ranking_config_dict(self) -> None:
        candidates = [
            {
                "name": "Frank",
                "analysis": {"resume_score": 10, "ats_score": 10},
                "matching": {"semantic_similarity": 0.1, "match_score": 5},
            },
        ]
        config = {"semantic_weight": 0.6, "resume_quality_weight": 0.2, "ats_weight": 0.1, "experience_weight": 0.05, "project_weight": 0.05}

        ranked = rank_candidates(candidates, config)

        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0]["rank"], 1)
        self.assertEqual(ranked[0]["candidate_name"], "Frank")


if __name__ == "__main__":
    unittest.main()
