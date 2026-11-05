import logging
import os
from datetime import datetime

import pytest

from .models import Query, RetrievalLog
from .retrieval_logic import retrieve_chunks

# --- Logger Setup ---
# Console logger
console_logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
console_logger.addHandler(console_handler)
console_logger.setLevel(logging.INFO)

# JSON File logger
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True) # Ensure the logs directory exists
log_file_path = os.path.join(log_dir, 'retrieval_verification.log')
file_logger = logging.getLogger('retrieval_logger')
file_handler = logging.FileHandler(log_file_path, mode='w')
# No formatter needed, we will log pre-formatted JSON strings
file_logger.addHandler(file_handler)
file_logger.setLevel(logging.INFO)
# --- End Logger Setup ---


# Placeholder for the sample queries.
SAMPLE_QUERIES: list[Query] = [
    Query(query_text="What are the core concepts of ROS 2?", expected_id="1-2-ros2-core-concepts.mdx"),
    Query(query_text="How do I create a ROS 2 workspace?", expected_id="1-3-ros2-workspace.mdx"),
    Query(query_text="What is a digital twin?", expected_id="2-1-introduction-to-digital-twins.mdx"),
    # Add more queries here...
]

@pytest.mark.parametrize("query", SAMPLE_QUERIES)
def test_retrieval_accuracy(query: Query):
    """
    Tests the accuracy of the RAG retrieval pipeline for a single query.
    """
    console_logger.info(f"Testing query: '{query.query_text}'")

    retrieved_chunks = retrieve_chunks(query.query_text, top_k=1)

    passed = False
    if retrieved_chunks:
        top_chunk = retrieved_chunks[0]
        console_logger.info(f"  - Top chunk source: {top_chunk.source_url}")
        console_logger.info(f"  - Score: {top_chunk.score:.4f}")

        if query.expected_id in top_chunk.source_url and top_chunk.score >= 0.80:
            passed = True

    # Log the result to the JSON file
    log_entry = RetrievalLog(
        timestamp=datetime.utcnow().isoformat(),
        query_text=query.query_text,
        passed=passed,
        retrieved_chunks=retrieved_chunks
    )
    file_logger.info(log_entry.model_dump_json())

    # Assertions
    assert retrieved_chunks, f"No chunks were retrieved for query: '{query.query_text}'"
    top_chunk = retrieved_chunks[0]
    assert query.expected_id in top_chunk.source_url, \
        f"Expected source '{query.expected_id}' not found in top chunk's source '{top_chunk.source_url}'"
    assert top_chunk.score >= 0.80, f"Score {top_chunk.score} is below the threshold of 0.80"

    console_logger.info(f"Query test PASSED for: '{query.query_text}'")
