import unittest
from unittest.mock import MagicMock, patch

from app.services.embedding import EmbeddingGenerator


class TestEmbeddingGenerator(unittest.TestCase):

    @patch('cohere.Client')
    def test_generate_embeddings(self, mock_cohere_client):
        # Mock the cohere client and its embed method
        mock_embed = MagicMock()
        mock_embed.return_value.embeddings = [[0.1, 0.2], [0.3, 0.4]]
        mock_cohere_client.return_value.embed = mock_embed

        generator = EmbeddingGenerator()
        embeddings = generator.generate_embeddings(["text1", "text2"])

        self.assertEqual(len(embeddings), 2)
        self.assertEqual(embeddings[0], [0.1, 0.2])

if __name__ == '__main__':
    unittest.main()
