import unittest

from app.services.text_processor import TextProcessor


class TestTextProcessor(unittest.TestCase):

    def test_clean_text(self):
        processor = TextProcessor()
        html = "<h1>Title</h1><p>This is a paragraph.</p>"
        cleaned_text = processor.clean_text(html)
        self.assertEqual(cleaned_text, "Title\n=====\n\nThis is a paragraph.")

    def test_chunk_text(self):
        processor = TextProcessor(chunk_size=5, chunk_overlap=1)
        text = "This is a test sentence for chunking."
        chunks = processor.chunk_text(text)

        # The exact output depends on the tokenizer, so we'll just check the number of chunks
        # and that they are strings.
        self.assertIsInstance(chunks, list)
        self.assertGreater(len(chunks), 1)
        self.assertIsInstance(chunks[0], str)

if __name__ == '__main__':
    unittest.main()

