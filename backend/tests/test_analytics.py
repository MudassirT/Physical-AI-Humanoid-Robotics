"""
Unit tests for the /analytics telemetry endpoint.
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def analytics_client(tmp_path: Path):
    """
    Returns a TestClient with ANALYTICS_LOG_PATH directed to a temporary file.
    """
    temp_log_file = tmp_path / "test_analytics.jsonl"
    with patch("app.routes.analytics.ANALYTICS_LOG_PATH", temp_log_file), \
         patch("app.routes.analytics.get_analytics_file_path", return_value=temp_log_file):
        client = TestClient(app)
        yield client, temp_log_file


class TestAnalyticsEndpoint:
    """Tests for POST /analytics and GET /analytics."""

    def test_post_analytics_event_records_successfully(self, analytics_client):
        client, log_file = analytics_client
        payload = {
            "event_type": "page_view",
            "session_id": "session-123",
            "module_id": "module1",
            "chapter_id": "1-1-intro",
            "data": {"referrer": "direct"},
        }
        response = client.post("/analytics", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "recorded"
        assert "event_id" in data

        # Verify entry on disk
        assert log_file.exists()
        lines = log_file.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert record["event_type"] == "page_view"
        assert record["session_id"] == "session-123"
        assert record["module_id"] == "module1"
        assert record["chapter_id"] == "1-1-intro"
        assert "timestamp" in record

    def test_post_analytics_validation_failure(self, analytics_client):
        client, _ = analytics_client
        # Missing required event_type
        response = client.post("/analytics", json={"session_id": "abc"})
        assert response.status_code == 422

    def test_get_analytics_summary_empty(self, analytics_client):
        client, log_file = analytics_client
        if log_file.exists():
            log_file.unlink()

        response = client.get("/analytics")
        assert response.status_code == 200
        data = response.json()
        assert data["total_events"] == 0
        assert data["event_counts"] == {}
        assert data["total_queries"] == 0
        assert data["popular_modules"] == {}
        assert data["average_quiz_scores"] == {}

    def test_get_analytics_summary_metrics(self, analytics_client):
        client, log_file = analytics_client

        # Post various events
        events = [
            {"event_type": "page_view", "module_id": "module1"},
            {"event_type": "page_view", "module_id": "module1"},
            {"event_type": "page_view", "module_id": "module6"},
            {"event_type": "query", "module_id": "module1", "data": {"q": "ros2"}},
            {"event_type": "query", "module_id": "module6", "data": {"q": "zmp"}},
            {
                "event_type": "quiz_score",
                "module_id": "module6",
                "chapter_id": "6-2-zero-moment-point",
                "data": {"score": 80.0},
            },
            {
                "event_type": "quiz_score",
                "module_id": "module6",
                "chapter_id": "6-2-zero-moment-point",
                "data": {"score": 100.0},
            },
        ]

        for ev in events:
            res = client.post("/analytics", json=ev)
            assert res.status_code == 200

        summary_res = client.get("/analytics")
        assert summary_res.status_code == 200
        summary = summary_res.json()

        assert summary["total_events"] == 7
        assert summary["event_counts"]["page_view"] == 3
        assert summary["event_counts"]["query"] == 2
        assert summary["event_counts"]["quiz_score"] == 2
        assert summary["total_queries"] == 2
        assert summary["popular_modules"]["module1"] == 3
        assert summary["popular_modules"]["module6"] == 4
        assert summary["average_quiz_scores"]["6-2-zero-moment-point"] == 90.0

    def test_get_analytics_skips_corrupted_lines(self, analytics_client):
        client, log_file = analytics_client
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, "w", encoding="utf-8") as f:
            f.write('{"event_type": "page_view", "module_id": "module1"}\n')
            f.write("CORRUPTED_NOT_A_JSON_LINE\n")
            f.write('{"event_type": "query", "module_id": "module1"}\n')

        summary_res = client.get("/analytics")
        assert summary_res.status_code == 200
        summary = summary_res.json()
        assert summary["total_events"] == 2
        assert summary["total_queries"] == 1
