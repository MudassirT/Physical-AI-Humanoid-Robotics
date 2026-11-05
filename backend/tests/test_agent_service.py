"""
Unit tests for app.agent.agent_service.AgentService

All Google Gemini API and RetrieverService calls are mocked.
Tests verify the agent loop logic, tool dispatch, and response shaping
without making real network requests.

Uses the ``google-genai`` SDK (google.genai.Client pattern).
"""

from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Helpers — build fake google.genai response objects
# ---------------------------------------------------------------------------


def _make_text_response(text: str):
    """
    Build a fake GenerateContentResponse that contains a single text part
    (no function calls) — represents the LLM's final answer.
    """
    part = MagicMock()
    part.text = text
    part.function_call = None  # no function call

    content = MagicMock()
    content.parts = [part]

    candidate = MagicMock()
    candidate.content = content

    response = MagicMock()
    response.candidates = [candidate]
    response.text = text
    return response


def _make_function_call_response(tool_name: str, args: dict):
    """
    Build a fake GenerateContentResponse that requests a function call —
    represents the LLM asking to invoke a tool.
    """
    fc = MagicMock()
    fc.name = tool_name
    fc.args = args

    part = MagicMock()
    part.text = None
    part.function_call = fc

    content = MagicMock()
    content.parts = [part]

    candidate = MagicMock()
    candidate.content = content

    response = MagicMock()
    response.candidates = [candidate]
    response.text = None
    return response


def _make_empty_response():
    """
    Build a fake response with no text and no function calls —
    simulates an empty reply.
    """
    part = MagicMock()
    part.text = ""
    part.function_call = None

    content = MagicMock()
    content.parts = [part]

    candidate = MagicMock()
    candidate.content = content

    response = MagicMock()
    response.candidates = [candidate]
    response.text = ""
    return response


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def agent_service():
    """
    Returns an AgentService instance with all external dependencies mocked:
    - google.genai.Client → mock (no real API calls)
    - RetrieverService → returns a single fake ContentChunk
    """
    from app.schemas.chat_models import ContentChunk

    fake_chunk = ContentChunk(
        chunk_id="1",
        source_url="https://example.com/ros2-nodes",
        original_text="A ROS 2 node is a process that performs computation.",
        score=0.92,
    )

    with patch("app.agent.agent_service.genai") as mock_genai, \
         patch("app.agent.agent_service.RetrieverService") as mock_retriever_cls:

        # --- Retriever mock ---
        mock_retriever_instance = MagicMock()
        mock_retriever_instance.retrieve_chunks.return_value = [fake_chunk]
        mock_retriever_cls.return_value = mock_retriever_instance

        # --- Gemini Client mock ---
        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client

        from app.agent.agent_service import AgentService
        service = AgentService()
        # Expose internals for test assertions
        service._mock_client = mock_client
        service._retriever_mock = mock_retriever_instance
        yield service


# ---------------------------------------------------------------------------
# Tests — AgentService.ask_agent
# ---------------------------------------------------------------------------


class TestAskAgent:
    """Tests for AgentService.ask_agent."""

    def test_returns_chat_response_on_direct_answer(self, agent_service):
        """Agent returns a ChatResponse when the LLM gives a direct text answer."""
        final_answer = "ROS 2 nodes are processes that do computation."
        agent_service._mock_client.models.generate_content.return_value = (
            _make_text_response(final_answer)
        )

        from app.schemas.chat_models import ChatResponse

        result = agent_service.ask_agent("What are ROS 2 nodes?")

        assert isinstance(result, ChatResponse)
        assert "ROS 2 nodes" in result.answer_text

    def test_calls_retrieve_chunks_tool_and_returns_answer(self, agent_service):
        """Agent performs one tool call then returns a synthesised answer."""
        tool_response = _make_function_call_response(
            "retrieve_chunks", {"query_text": "What are ROS 2 nodes?", "top_k": 5}
        )
        final_response = _make_text_response(
            "Nodes are the building blocks of ROS 2."
        )

        # First call → tool call; second call → final text
        agent_service._mock_client.models.generate_content.side_effect = [
            tool_response,
            final_response,
        ]

        result = agent_service.ask_agent("What are ROS 2 nodes?")

        assert result.answer_text == "Nodes are the building blocks of ROS 2."
        # Retriever must have been called once
        agent_service._retriever_mock.retrieve_chunks.assert_called_once()

    def test_sources_extracted_from_tool_output(self, agent_service):
        """Retrieved source URLs are propagated into ChatResponse.retrieved_sources."""
        tool_response = _make_function_call_response(
            "retrieve_chunks", {"query_text": "What are ROS 2 nodes?"}
        )
        final_response = _make_text_response("Nodes perform computation in ROS 2.")

        agent_service._mock_client.models.generate_content.side_effect = [
            tool_response,
            final_response,
        ]

        result = agent_service.ask_agent("What are ROS 2 nodes?")

        # The fake chunk has source_url = "https://example.com/ros2-nodes"
        assert any("ros2-nodes" in src for src in result.retrieved_sources)

    def test_returns_fallback_on_max_turns_exceeded(self, agent_service):
        """Agent returns a graceful fallback if it never produces a text answer."""
        always_tool = _make_function_call_response(
            "retrieve_chunks", {"query_text": "looping question"}
        )
        # Always returns a tool call, never a final text answer
        agent_service._mock_client.models.generate_content.return_value = always_tool

        result = agent_service.ask_agent("Question that loops forever")

        assert "could not generate a response" in result.answer_text.lower()

    def test_returns_fallback_when_llm_returns_empty_message(self, agent_service):
        """Empty content and no function_call → graceful fallback, not an exception."""
        agent_service._mock_client.models.generate_content.return_value = (
            _make_empty_response()
        )

        result = agent_service.ask_agent("Test question")

        assert result.answer_text  # non-empty string
        assert isinstance(result.answer_text, str)

    def test_unknown_tool_call_is_handled_gracefully(self, agent_service):
        """An unknown tool name should not crash the agent."""
        unknown_tool_response = _make_function_call_response(
            "some_unknown_tool", {"foo": "bar"}
        )
        final_response = _make_text_response("I cannot answer that.")

        agent_service._mock_client.models.generate_content.side_effect = [
            unknown_tool_response,
            final_response,
        ]

        result = agent_service.ask_agent("Trigger unknown tool")

        # Should not raise; answer should still come through
        assert isinstance(result.answer_text, str)


# ---------------------------------------------------------------------------
# Tests — AgentService._call_tool
# ---------------------------------------------------------------------------


class TestCallTool:
    """Unit tests for the internal _call_tool dispatcher."""

    def _make_function_call(self, name: str, args: dict):
        """Build a minimal fake FunctionCall object."""
        fc = MagicMock()
        fc.name = name
        fc.args = args
        return fc

    def test_retrieve_chunks_tool_returns_formatted_string(self, agent_service):
        fc = self._make_function_call(
            "retrieve_chunks", {"query_text": "What is Isaac Sim?", "top_k": 5}
        )
        output = agent_service._call_tool(fc)

        assert output.tool_name == "retrieve_chunks"
        assert "Source:" in output.output
        assert "Content:" in output.output

    def test_retrieve_chunks_tool_handles_no_results(self, agent_service):
        agent_service._retriever_mock.retrieve_chunks.return_value = []
        fc = self._make_function_call(
            "retrieve_chunks", {"query_text": "Unknown topic"}
        )
        output = agent_service._call_tool(fc)

        assert "No relevant information" in output.output

    def test_retrieve_chunks_missing_query_text_returns_error(self, agent_service):
        """Calling retrieve_chunks without query_text should return an error message."""
        fc = self._make_function_call("retrieve_chunks", {})
        output = agent_service._call_tool(fc)

        assert "Error" in output.output

    def test_unknown_tool_returns_error_output(self, agent_service):
        """An unknown tool name should return an error ToolOutput, not raise."""
        fc = self._make_function_call("completely_unknown_tool", {"foo": "bar"})
        output = agent_service._call_tool(fc)

        assert "Unknown tool" in output.output
        assert output.tool_name == "completely_unknown_tool"
