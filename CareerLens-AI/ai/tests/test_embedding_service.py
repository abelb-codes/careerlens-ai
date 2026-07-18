"""Unit tests for the matcher embedding service."""

from __future__ import annotations

import unittest

from ai.matcher.embedding_service import SentenceTransformerEmbeddingService


class TestEmbeddingService(unittest.TestCase):
    """Tests for embedding service behavior."""

    def test_encode_returns_embeddings_for_texts(self) -> None:
        service = SentenceTransformerEmbeddingService()
        embeddings = service.encode(["Resume NLP", "Job description analysis"])

        self.assertEqual(embeddings.shape[0], 2)
        self.assertGreater(embeddings.shape[1], 0)

    def test_encode_ignores_non_strings(self) -> None:
        service = SentenceTransformerEmbeddingService()
        embeddings = service.encode(["Valid text", 123, None])

        self.assertEqual(embeddings.shape[0], 1)
        self.assertGreater(embeddings.shape[1], 0)

    def test_encode_invalid_input_returns_empty_array(self) -> None:
        service = SentenceTransformerEmbeddingService()
        embeddings = service.encode(None)  # type: ignore[arg-type]

        self.assertEqual(embeddings.shape, (0, 0))


if __name__ == "__main__":
    unittest.main()
