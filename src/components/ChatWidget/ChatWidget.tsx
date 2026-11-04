/**
 * ChatWidget — React component that provides an interactive Q&A interface
 * powered by the FastAPI RAG Agent backend.
 *
 * Features:
 * - Sends user queries to POST /ask on the configured backend.
 * - Displays user and agent messages in a scrollable chat history.
 * - Shows a loading indicator while awaiting the agent's response.
 * - Displays source citations from the agent's retrieved context.
 * - Handles network errors gracefully with user-friendly messages.
 * - Prevents submission of empty queries.
 * - Automatically scrolls to the latest message.
 * - Keyboard accessible (Enter to send, Shift+Enter for newline future support).
 * - ARIA live region for screen reader announcements.
 *
 * Environment configuration:
 *   REACT_APP_FASTAPI_BASE_URL — Override the backend URL (default: http://127.0.0.1:8000)
 */

import React, { useState, useRef, useEffect, useCallback } from 'react';
import styles from './ChatWidget.module.css';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'agent' | 'system';
  timestamp: Date;
  sources?: string[];
}

interface AskResponse {
  answer_text: string;
  retrieved_sources: string[];
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Returns the backend base URL from the injected environment variable,
 * falling back to localhost for local development.
 */
function getBackendUrl(): string {
  // process.env.REACT_APP_FASTAPI_BASE_URL is injected by docusaurus.config.ts
  // via the custom webpack DefinePlugin.
  return (process.env.REACT_APP_FASTAPI_BASE_URL as string | undefined) ?? 'http://127.0.0.1:8000';
}

function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

const ChatWidget: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Ref to the bottom of the message list — used for auto-scroll.
  const messagesEndRef = useRef<HTMLDivElement>(null);

  /** Scroll the message area to the latest message. */
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // ------------------------------------------------------------------
  // Send message handler
  // ------------------------------------------------------------------

  const handleSendMessage = useCallback(async () => {
    const trimmed = inputMessage.trim();
    if (!trimmed || isLoading) return;

    // Append the user's message immediately.
    const userMessage: ChatMessage = {
      id: generateId(),
      text: trimmed,
      sender: 'user',
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const backendUrl = getBackendUrl();
      const response = await fetch(`${backendUrl}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({ query_text: trimmed }),
      });

      if (!response.ok) {
        // Try to surface the FastAPI error detail.
        let detail = `HTTP ${response.status}`;
        try {
          const errData = await response.json();
          detail = errData.detail ?? detail;
        } catch {
          // Ignore JSON parse failure — keep the status code message.
        }
        throw new Error(detail);
      }

      const data: AskResponse = await response.json();

      const agentMessage: ChatMessage = {
        id: generateId(),
        text: data.answer_text,
        sender: 'agent',
        timestamp: new Date(),
        sources: data.retrieved_sources?.length > 0 ? data.retrieved_sources : undefined,
      };
      setMessages((prev) => [...prev, agentMessage]);
    } catch (error) {
      console.error('[ChatWidget] Error sending message:', error);
      const errorText =
        error instanceof Error
          ? `Error: ${error.message}`
          : 'An unknown error occurred. Please try again.';
      const systemMessage: ChatMessage = {
        id: generateId(),
        text: errorText,
        sender: 'system',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, systemMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [inputMessage, isLoading]);

  // Handle Enter key (without Shift) to submit.
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
        e.preventDefault();
        handleSendMessage();
      }
    },
    [handleSendMessage, isLoading],
  );

  // ------------------------------------------------------------------
  // Render
  // ------------------------------------------------------------------

  return (
    <div className={styles.chatContainer} role="region" aria-label="RAG Chat Assistant">
      {/* Header */}
      <div className={styles.chatHeader}>
        <span>🤖 RAG Assistant — Ask about the book</span>
      </div>

      {/* Message area — ARIA live region so screen readers announce new messages */}
      <div
        className={styles.messageDisplay}
        role="log"
        aria-live="polite"
        aria-atomic="false"
        aria-label="Chat messages"
      >
        {messages.length === 0 && (
          <div className={styles.emptyState}>
            Ask me anything about <strong>Physical AI &amp; Humanoid Robotics</strong>!
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`${styles.messageBubble} ${styles[message.sender]}`}
            role="article"
            aria-label={`${message.sender === 'user' ? 'You' : message.sender === 'agent' ? 'Agent' : 'System'}: ${message.text}`}
          >
            <div className={styles.messageSender}>
              {message.sender === 'user' ? 'You' : message.sender === 'agent' ? '🤖 Agent' : '⚠️ System'}
            </div>
            <div className={styles.messageText}>{message.text}</div>

            {/* Source citations */}
            {message.sources && message.sources.length > 0 && (
              <div className={styles.messageSources}>
                <span className={styles.sourcesLabel}>Sources:</span>
                {message.sources.map((source, index) => (
                  <a
                    key={index}
                    href={source}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={styles.sourceLink}
                    aria-label={`Source ${index + 1}: ${source}`}
                  >
                    [{index + 1}]
                  </a>
                ))}
              </div>
            )}

            <div className={styles.messageTimestamp} aria-hidden="true">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}

        {/* Loading indicator */}
        {isLoading && (
          <div className={styles.loadingIndicator} role="status" aria-live="assertive">
            <span className={styles.loadingDots}>Agent is thinking</span>
            <span aria-hidden="true">…</span>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className={styles.inputArea}>
        <input
          type="text"
          className={styles.messageInput}
          placeholder="Ask a question about the book…"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          aria-label="Type your question here"
          aria-disabled={isLoading}
          maxLength={1000}
        />
        <button
          className={styles.sendButton}
          onClick={handleSendMessage}
          disabled={isLoading || !inputMessage.trim()}
          aria-label="Send message"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatWidget;
