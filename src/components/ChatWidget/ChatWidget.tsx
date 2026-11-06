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
// SVG Icons
// ---------------------------------------------------------------------------

function BotIcon() {
  return (
    <svg className={styles.chatHeaderIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="11" width="18" height="10" rx="2" />
      <circle cx="12" cy="5" r="2" />
      <path d="M12 7v4" />
      <line x1="8" y1="16" x2="8" y2="16" />
      <line x1="16" y1="16" x2="16" y2="16" />
    </svg>
  );
}

function TrashIcon() {
  return (
    <svg className={styles.clearIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 6h18" />
      <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
      <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
    </svg>
  );
}

function SendIcon() {
  return (
    <svg className={styles.sendIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="22" y1="2" x2="11" y2="13" />
      <polygon points="22 2 15 22 11 13 2 9 22 2" />
    </svg>
  );
}

function ExternalLinkIcon() {
  return (
    <svg className={styles.sourceIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
      <polyline points="15 3 21 3 21 9" />
      <line x1="10" y1="14" x2="21" y2="3" />
    </svg>
  );
}

function SparklesIcon() {
  return (
    <svg className={styles.suggestionsHeaderIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" />
    </svg>
  );
}

function ChevronRightIcon() {
  return (
    <svg className={styles.promptCardArrow} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <polyline points="9 18 15 12 9 6" />
    </svg>
  );
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

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

interface SuggestedPrompt {
  topic: string;
  query: string;
}

const SUGGESTED_PROMPTS: SuggestedPrompt[] = [
  { topic: 'Module 1 • ROS 2', query: 'What is the ROS 2 DDS middleware layer and QoS?' },
  { topic: 'Module 2 • Simulation', query: 'How do Gazebo and Unity simulate Digital Twins?' },
  { topic: 'Module 4 • VLA', query: 'How do Vision-Language-Action (VLA) models work in humanoid robotics?' },
];

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

  // Clear chat
  const handleClear = useCallback(() => {
    setMessages([WELCOME_MESSAGE]);
    inputRef.current?.focus();
  }, []);

  // Send message handler (supports direct invocation from suggestion cards)
  const handleSendMessage = useCallback(async (customQuery?: string) => {
    const trimmed = (customQuery ?? inputMessage).trim();
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
          // Ignore JSON parse failure
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

  // Handle Enter key to submit
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
        e.preventDefault();
        handleSendMessage();
      }
    },
    [handleSendMessage, isLoading],
  );

  return (
    <div className={styles.chatContainer} role="region" aria-label="RAG Chat Assistant">
      {/* ---- Header ---- */}
      <div className={styles.chatHeader}>
        <div className={styles.chatHeaderLeft}>
          <div className={styles.chatHeaderIconWrapper}>
            <BotIcon />
          </div>
          <div>
            <div className={styles.chatHeaderTitle}>RAG Assistant</div>
            <div className={styles.chatHeaderSub}>Physical AI & Humanoid Robotics</div>
          </div>
        </div>

        <div className={styles.chatHeaderRight}>
          {/* Online status */}
          <div className={styles.statusDot}>
            <div className={styles.statusDotCircle} />
            {isLoading ? 'Thinking…' : 'Online'}
          </div>

          {/* Clear chat */}
          <button
            className={styles.clearButton}
            onClick={handleClear}
            aria-label="Clear chat history"
            title="Clear chat"
          >
            <TrashIcon />
            <span>Clear</span>
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
        {messages.map((message) => (
          <div
            key={message.id}
            className={`${styles.messageBubble} ${styles[message.sender]}`}
            role="article"
            aria-label={`${message.sender === 'user' ? 'You' : message.sender === 'agent' ? 'Agent' : 'System'}: ${message.text}`}
          >
            <div className={styles.messageSender}>
              {message.sender === 'user' ? 'You' : message.sender === 'agent' ? 'AI Assistant' : 'System Notice'}
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
                    <span>[{index + 1}]</span>
                    <ExternalLinkIcon />
                  </a>
                ))}
              </div>
            )}

            <div className={styles.messageTimestamp} aria-hidden="true">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}

        {/* Suggested Quick Prompts on initial load — compact horizontal grid without inner scroll */}
        {messages.length === 1 && (
          <div className={styles.suggestionsWrapper}>
            <div className={styles.suggestionsHeader}>
              <SparklesIcon />
              <span>Suggested starter questions grounded in the book:</span>
            </div>
            <div className={styles.promptGrid}>
              {SUGGESTED_PROMPTS.map((p, idx) => (
                <button
                  key={idx}
                  type="button"
                  className={styles.promptCard}
                  onClick={() => handleSendMessage(p.query)}
                  disabled={isLoading}
                >
                  <div className={styles.promptCardContent}>
                    <span className={styles.promptBadge}>{p.topic}</span>
                    <span className={styles.promptText}>{p.query}</span>
                  </div>
                  <ChevronRightIcon />
                </button>
              ))}
            </div>
          </div>
        )}

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
          placeholder="Ask a technical question about any chapter…"
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
          onClick={() => handleSendMessage()}
          disabled={isLoading || !inputMessage.trim()}
          aria-label="Send message"
        >
          <SendIcon />
          <span className={styles.sendButtonLabel}>Send</span>
        </button>
      </div>
    </div>
  );
};

export default ChatWidget;
