/**
 * ChatWidget — React component that provides an interactive Q&A interface
 * powered by the FastAPI RAG Agent backend.
 *
 * Features:
 * - Sends user queries to POST /ask on the configured backend.
 * - Displays user and agent messages in a scrollable chat history.
 * - Shows a pulsing typing indicator while awaiting a response.
 * - Displays source citations from the agent's retrieved context.
 * - Handles network errors gracefully with user-friendly messages.
 * - Prevents submission of empty queries.
 * - Automatically scrolls to the latest message.
 * - Keyboard accessible (Enter to send).
 * - ARIA live region for screen reader announcements.
 * - Clear chat button.
 * - Welcome message on first load.
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
  return (process.env.REACT_APP_FASTAPI_BASE_URL as string | undefined) ?? 'http://127.0.0.1:8000';
}

function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

const WELCOME_MESSAGE: ChatMessage = {
  id: 'welcome',
  text: 'Hello! I\'m your RAG-powered AI assistant for the Physical AI & Humanoid Robotics book. Ask me anything about ROS 2, Digital Twins, NVIDIA Isaac, Vision-Language-Action models, and more!',
  sender: 'agent',
  timestamp: new Date(),
};

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

const ChatWidget: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME_MESSAGE]);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  /** Scroll the message area to the latest message. */
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // ------------------------------------------------------------------
  // Clear chat
  // ------------------------------------------------------------------
  const handleClear = useCallback(() => {
    setMessages([WELCOME_MESSAGE]);
    inputRef.current?.focus();
  }, []);

  // ------------------------------------------------------------------
  // Send message handler
  // ------------------------------------------------------------------

  const handleSendMessage = useCallback(async () => {
    const trimmed = inputMessage.trim();
    if (!trimmed || isLoading) return;

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
      {/* ---- Header ---- */}
      <div className={styles.chatHeader}>
        <div className={styles.chatHeaderLeft}>
          <div className={styles.chatHeaderIconWrapper}><svg className={styles.chatHeaderIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="11" width="18" height="10" rx="2" /><circle cx="12" cy="5" r="2" /><path d="M12 7v4" /></svg></div>
          <div>
            <div className={styles.chatHeaderTitle}>RAG Assistant</div>
            <div className={styles.chatHeaderSub}>Physical AI & Humanoid Robotics</div>
          </div>
        </div>

        <div className={styles.chatHeaderRight}>
          {/* Online status */}
          <div className={styles.statusDot}>
            <div className={`${styles.statusDotCircle} ${isLoading ? '' : ''}`} />
            {isLoading ? 'Thinking…' : 'Online'}
          </div>

          {/* Clear chat */}
          <button
            className={styles.clearButton}
            onClick={handleClear}
            aria-label="Clear chat history"
            title="Clear chat"
          >
            Clear
          </button>
        </div>
      </div>

      {/* ---- Message area — ARIA live region ---- */}
      <div
        className={styles.messageDisplay}
        role="log"
        aria-live="polite"
        aria-atomic="false"
        aria-label="Chat messages"
      >
        {messages.length === 0 && (
          <div className={styles.emptyState}>
            <span className={styles.emptyStateIcon}>💬</span>
            <p className={styles.emptyStateText}>
              Ask me anything about <strong>Physical AI & Humanoid Robotics</strong>!
            </p>
            <p className={styles.emptyStateHint}>
              Try: "What is ROS 2?" or "Explain Vision-Language-Action models"
            </p>
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

        {/* Pulsing typing indicator */}
        {isLoading && (
          <div className={styles.loadingIndicator} role="status" aria-live="assertive" aria-label="Agent is thinking">
            <div className={styles.typingDots}>
              <span /><span /><span />
            </div>
            Agent is thinking…
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>

      {/* ---- Input area ---- */}
      <div className={styles.inputArea}>
        <input
          ref={inputRef}
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
          <span className={styles.sendIcon}>&gt;</span>
          <span className={styles.sendButtonLabel}>Send</span>
        </button>
      </div>
    </div>
  );
};

export default ChatWidget;
