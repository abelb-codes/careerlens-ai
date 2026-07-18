"""Unit tests for the matcher similarity utilities."""

from __future__ import annotations

import unittest

import numpy as np

from ai.matcher.similarity import compute_semantic_similarity, compare_term_sets, coverage_ratio


class TestSimilarityUtilities(unittest.TestCase):
    """Test cases for semantic similarity and term coverage."""

    def test_compute_semantic_similarity_returns_one_for_identical_vectors(self) -> None:
        embeddings = np.array([[1.0, 0.0, 0.0], [1.0, 0.0, 0.0]])
        score = compute_semantic_similarity(embeddings)

        self.assertEqual(score, 1.0)

    def test_compute_semantic_similarity_returns_zero_for_orthogonal_vectors(self) -> None:
        embeddings = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        score = compute_semantic_similarity(embeddings)

        self.assertEqual(score, 0.0)

    def test_compute_semantic_similarity_invalid_input_returns_zero(self) -> None:
        score = compute_semantic_similarity(np.array([1.0, 2.0, 3.0]))

        self.assertEqual(score, 0.0)

    def test_compare_term_sets_matches_terms_and_reports_missing(self) -> None:
        matched, missing = compare_term_sets(
            ["Python", "Django", "AWS"],
            ["django", "python"],
        )

        self.assertEqual(matched, ["python", "django"])
        self.assertEqual(missing, ["aws"])

    def test_coverage_ratio_calculates_expected_fraction(self) -> None:
        matched = ["python", "django"]
        ratio = coverage_ratio(["python", "django", "aws"], matched)

        self.assertAlmostEqual(ratio, 2 / 3)

    def test_coverage_ratio_empty_required_returns_one(self) -> None:
        ratio = coverage_ratio([], [])

        self.assertEqual(ratio, 1.0)


if __name__ == "__main__":
    unittest.main()
