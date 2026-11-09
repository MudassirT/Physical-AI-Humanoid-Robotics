import React, { useState, useRef, useEffect, useCallback, useMemo } from 'react';
import useIsBrowser from '@docusaurus/useIsBrowser';
import styles from './styles.module.css';

// ---------------------------------------------------------------------------
// Types & Interfaces
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

interface QuickPrompt {
  tag: string;
  query: string;
}

const GENERAL_PROMPTS: QuickPrompt[] = [
  { tag: 'ROS 2 DDS', query: 'What are ROS 2 QoS policies for low-latency humanoid motor control?' },
  { tag: 'Digital Twin', query: 'How do Gazebo and Unity simulate contact dynamics and sensors?' },
  { tag: 'NVIDIA Isaac', query: 'How does Isaac ROS cuVSLAM calculate visual-inertial odometry?' },
  { tag: 'VLA Planning', query: 'How do Vision-Language-Action (VLA) models convert voice into robot trajectories?' },
];

const MODULE1_PROMPTS: QuickPrompt[] = [
  { tag: 'ROS 2 QoS', query: 'What is the difference between Best Effort and Reliable QoS in ROS 2 motor loops?' },
  { tag: 'Iceoryx IPC', query: 'How does Eclipse Iceoryx shared memory achieve zero-copy message passing?' },
  { tag: 'Lifecycle Nodes', query: 'Explain the ROS 2 lifecycle node state transitions for actuator safety.' },
  { tag: 'Real-Time Control', query: 'How do lockless ring buffers prevent jitter in 1 kHz control loops?' },
];

const MODULE2_PROMPTS: QuickPrompt[] = [
  { tag: 'Gazebo Physics', query: 'How do Gazebo Harmonic and DART calculate contact friction for bipedal feet?' },
  { tag: 'URDF vs SDF', query: 'What is the structural difference between URDF, Xacro, and SDF formats in humanoid modeling?' },
  { tag: 'Sim-to-Real', query: 'How does physics domain randomization bridge the reality gap before hardware deployment?' },
  { tag: 'Unity HDRP', query: 'How does Unity HDRP connect to ROS 2 topics via ROS-TCP-Connector?' },
];

const MODULE3_PROMPTS: QuickPrompt[] = [
  { tag: 'Isaac cuVSLAM', query: 'How does NVIDIA cuVSLAM compute stereo visual-inertial odometry with low drift?' },
  { tag: 'NITROS Acceleration', query: 'What is the NITROS zero-copy GPU memory exchange in Isaac ROS?' },
  { tag: 'Nav2 Bipedal', query: 'How does Nav2 bipedal footstep planning navigate 3D elevation maps?' },
  { tag: 'Synthetic Data', query: 'How does Isaac Sim Replicator generate synthetic data with domain randomization?' },
];

const MODULE4_PROMPTS: QuickPrompt[] = [
  { tag: 'OpenVLA Architecture', query: 'How does OpenVLA translate multimodal vision and language into joint actions?' },
  { tag: 'Action Chunking', query: 'What is action chunking and why is it essential for 50 Hz humanoid control?' },
  { tag: 'Voice-to-Action', query: 'How does Whisper voice-to-action decompose high-level commands into subtasks?' },
  { tag: '3D Affordance', query: 'How does 3D spatial grounding predict grasp affordances for humanoid dexterous hands?' },
];

const MODULE5_PROMPTS: QuickPrompt[] = [
  { tag: 'Forward Kinematics', query: 'How does the Product of Exponentials (PoE) Lie group formulation improve humanoid forward kinematics?' },
  { tag: 'Inverse Kinematics', query: 'How does null-space projection resolve kinematic redundancy for 7-DOF humanoid arms?' },
  { tag: 'Rigid Body Dynamics', query: 'How does Featherstone Articulated Body Algorithm (ABA) achieve O(n) forward dynamics?' },
  { tag: 'Spatial Vectors', query: 'Explain 6D spatial vector algebra for spatial velocity, force, and spatial inertia.' },
];

const MODULE6_PROMPTS: QuickPrompt[] = [
  { tag: 'Zero-Moment Point', query: 'Derive the 3D Linear Inverted Pendulum Model (3D-LIPM) and Kajita preview control equations.' },
  { tag: 'Capture Point', query: 'How do Instantaneous Capture Point (ICP) and Divergent Component of Motion (DCM) stabilize bipedal push recovery?' },
  { tag: 'Convex MPC', query: 'How does real-time convex MPC compute ground reaction forces at 500 Hz for legged locomotion?' },
  { tag: 'Whole-Body Control', query: 'How does QP-based whole-body control enforce contact friction cone constraints?' },
];

const MODULE7_PROMPTS: QuickPrompt[] = [
  { tag: 'Grasp Theory', query: 'What is the mathematical condition for force closure in grasp wrench space analysis?' },
  { tag: 'Hand Design', query: 'Compare tendon-driven underactuated hands with fully actuated dexterous hands.' },
  { tag: 'GelSight Tactile', query: 'How does GelSight optical tactile sensing reconstruct high-resolution contact depth?' },
  { tag: 'MoveIt 2', query: 'How does MoveIt 2 integrate OMPL and Riemannian Motion Policies for obstacle avoidance?' },
];

const MODULE8_PROMPTS: QuickPrompt[] = [
  { tag: 'PPO for Locomotion', query: 'Explain PPO clipped surrogate objective and reward shaping for humanoid walking.' },
  { tag: 'Isaac Lab Scale', query: 'How does Isaac Lab train 4,096 vectorized GPU environments in parallel?' },
  { tag: 'Curriculum Learning', query: 'How does automatic curriculum learning schedule progressive terrain difficulty?' },
  { tag: 'World Models', query: 'How do latent world models like Dreamer V3 enable sample-efficient robot learning?' },
];

const MODULE9_PROMPTS: QuickPrompt[] = [
  { tag: 'Reality Gap', query: 'What are the primary sources of the sim-to-real gap in humanoid locomotion and manipulation?' },
  { tag: 'Domain Randomization', query: 'How does Adaptive Domain Randomization (ADR) expand parameter ranges during training?' },
  { tag: 'Rapid Motor Adaptation', query: 'How does the RMA two-stage teacher-student architecture adapt to unknown friction online?' },
  { tag: 'System Identification', query: 'How are actuator dynamics and LuGre friction identified from robot telemetry logs?' },
];

const MODULE10_PROMPTS: QuickPrompt[] = [
  { tag: 'QDD Actuators', query: 'Why are Quasi-Direct Drive (QDD) actuators preferred for high-impact bipedal legs?' },
  { tag: 'Field Oriented Control', query: 'Explain the Clarke and Park transforms in Field Oriented Control (FOC) motor inverters.' },
  { tag: 'EtherCAT & CAN-FD', query: 'Why is EtherCAT preferred over CAN-FD for sub-millisecond 1 kHz joint synchronization?' },
  { tag: 'Jetson Compute', query: 'How does the NVIDIA Jetson AGX Orin split workloads across CPU, Tensor Cores, and DLAs?' },
];

const MODULE11_PROMPTS: QuickPrompt[] = [
  { tag: 'Safety Standards', query: 'How do ISO 10218, ISO/TS 15066, and ISO 13849 apply to humanoid robot safety?' },
  { tag: 'Physical HRI', query: 'How do momentum observers and power-and-force limiting prevent injury during human contact?' },
  { tag: 'Functional Safety', query: 'Explain Safety Integrity Level (SIL 2) dual-channel architecture for humanoid E-stops.' },
  { tag: 'Ethics & Privacy', query: 'What are the privacy and data governance requirements for autonomous humanoids in public spaces?' },
];

const MODULE12_PROMPTS: QuickPrompt[] = [
  { tag: 'Full-Stack Capstone', query: 'Outline the architectural pipeline for an autonomous tabletop manipulation capstone.' },
  { tag: 'Loco-Manipulation', query: 'What are the key research frontiers in simultaneous bipedal walking and manipulation?' },
  { tag: 'Gaussian Splatting', query: 'How does 3D Gaussian Splatting enable real-time novel view synthesis for robot perception?' },
  { tag: 'Humanoid Roadmap', query: 'What are the projected engineering milestones for general-purpose humanoids through 2030?' },
];

function formatSourceUrl(src: string): string {
  return src.replace(/\.mdx?$/, '');
}

function formatSourceLabel(src: string, index: number): string {
  const clean = src.replace(/\.mdx?$/, '');
  const parts = clean.split('/').filter(Boolean);
  const last = parts[parts.length - 1];
  if (!last || last === 'intro') return 'Introduction';
  const match = last.match(/^(\d+)-(\d+)-(.*)$/);
  if (match) {
    const topic = match[3].replace(/-/g, ' ');
    return `Ch ${match[1]}.${match[2]}: ${topic.charAt(0).toUpperCase() + topic.slice(1)}`;
  }
  return last.replace(/-/g, ' ');
}

function getBackendUrl(): string {
  return (process.env.REACT_APP_FASTAPI_BASE_URL as string | undefined) ?? 'http://127.0.0.1:8000';
}

function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

// ---------------------------------------------------------------------------
// SVG Icons
// ---------------------------------------------------------------------------

function SparkleBotIcon() {
  return (
    <svg className={styles.botIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 2a4 4 0 0 0-4 4v1H6a3 3 0 0 0-3 3v8a3 3 0 0 0 3 3h12a3 3 0 0 0 3-3v-8a3 3 0 0 0-3-3h-2V6a4 4 0 0 0-4-4Z" />
      <circle cx="9" cy="13" r="1.5" fill="currentColor" />
      <circle cx="15" cy="13" r="1.5" fill="currentColor" />
      <path d="M10 17h4" />
      <path d="M12 2v2" />
    </svg>
  );
}

function CloseIcon() {
  return (
    <svg className={styles.actionIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="18" y1="6" x2="6" y2="18" />
      <line x1="6" y1="6" x2="18" y2="18" />
    </svg>
  );
}

function TrashIcon() {
  return (
    <svg className={styles.actionIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
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

function CopyIcon() {
  return (
    <svg className={styles.copyIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
    </svg>
  );
}

function CheckIcon() {
  return (
    <svg className={styles.copyIcon} viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <polyline points="20 6 9 17 4 12" />
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
    <svg className={styles.sparklesIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" />
    </svg>
  );
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function FloatingAssistant(): React.ReactElement | null {
  const isBrowser = useIsBrowser();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      text: 'Hello! I am your AI Robotics Tutor. I am grounded in all 110 chapters across 12 modules of this curriculum. Ask me anything about ROS 2, Gazebo & Unity digital twins, NVIDIA Isaac perception, Vision-Language-Action systems, bipedal locomotion, or robot learning!',
      sender: 'agent',
      timestamp: new Date(),
    },
  ]);
  const [inputQuery, setInputQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Determine context-aware prompts based on the current chapter / module path
  const contextualPrompts = useMemo<QuickPrompt[]>(() => {
    if (!isBrowser || typeof window === 'undefined') return GENERAL_PROMPTS;
    const path = window.location.pathname;

    if (path.includes('module1-ros2')) return MODULE1_PROMPTS;
    if (path.includes('module2-digital-twin')) return MODULE2_PROMPTS;
    if (path.includes('module3-ai-robot-brain')) return MODULE3_PROMPTS;
    if (path.includes('module4-vla')) return MODULE4_PROMPTS;
    if (path.includes('module5-kinematics')) return MODULE5_PROMPTS;
    if (path.includes('module6-bipedal')) return MODULE6_PROMPTS;
    if (path.includes('module7-dexterous')) return MODULE7_PROMPTS;
    if (path.includes('module8-robot')) return MODULE8_PROMPTS;
    if (path.includes('module9-sim')) return MODULE9_PROMPTS;
    if (path.includes('module10-hardware')) return MODULE10_PROMPTS;
    if (path.includes('module11-safety')) return MODULE11_PROMPTS;
    if (path.includes('module12-capstone')) return MODULE12_PROMPTS;
    return GENERAL_PROMPTS;
  }, [isBrowser, isOpen]);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
      setTimeout(() => inputRef.current?.focus(), 150);
    }
  }, [isOpen, messages, scrollToBottom]);

  // Keyboard shortcut: Ctrl+K or Cmd+K toggles the drawer, Escape closes it
  useEffect(() => {
    if (!isBrowser) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsOpen((prev) => !prev);
      } else if (e.key === 'Escape' && isOpen) {
        setIsOpen(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isBrowser, isOpen]);

  const handleCopy = useCallback(async (msgId: string, text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedId(msgId);
      setTimeout(() => setCopiedId(null), 2000);
    } catch {
      // Ignore clipboard write failure
    }
  }, []);

  const handleClear = useCallback(() => {
    setMessages([
      {
        id: 'welcome',
        text: 'Chat history cleared. How can I help you explore the robotics curriculum today?',
        sender: 'agent',
        timestamp: new Date(),
      },
    ]);
  }, []);

  const handleSendMessage = useCallback(async (customQuery?: string) => {
    const query = (customQuery ?? inputQuery).trim();
    if (!query || isLoading) return;

    const userMessage: ChatMessage = {
      id: generateId(),
      text: query,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputQuery('');
    setIsLoading(true);

    try {
      const backendUrl = getBackendUrl();
      let currentModule: string | undefined;
      if (typeof window !== 'undefined') {
        const match = window.location.pathname.match(/module(\d+)/i);
        if (match) currentModule = `module${match[1]}`;
      }

      const response = await fetch(`${backendUrl}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'text/event-stream, application/json',
        },
        body: JSON.stringify({
          query_text: query,
          stream: true,
          module_filter: currentModule,
        }),
      });

      if (!response.ok) {
        let detail = `Server returned ${response.status}`;
        try {
          const errData = await response.json();
          detail = errData.detail ?? detail;
        } catch {
          // ignore error parse
        }
        throw new Error(detail);
      }

      const contentType = response.headers.get('content-type') || '';
      if (contentType.includes('text/event-stream') && response.body) {
        // SSE Streaming Handler
        const agentMsgId = generateId();
        let streamedText = '';
        let streamedSources: string[] | undefined = undefined;

        setMessages((prev) => [
          ...prev,
          {
            id: agentMsgId,
            text: '',
            sender: 'agent',
            timestamp: new Date(),
          },
        ]);

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let buffer = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });
          const parts = buffer.split('\n\n');
          buffer = parts.pop() || '';

          for (const block of parts) {
            const trimmed = block.trim();
            if (!trimmed) continue;
            let eventType = 'message';
            let eventData = '';

            for (const line of trimmed.split('\n')) {
              if (line.startsWith('event:')) {
                eventType = line.replace('event:', '').trim();
              } else if (line.startsWith('data:')) {
                eventData = line.replace('data:', '').trim();
              }
            }

            if (eventType === 'sources') {
              try {
                const parsed = JSON.parse(eventData);
                if (parsed.sources && Array.isArray(parsed.sources)) {
                  streamedSources = parsed.sources;
                }
              } catch {
                // ignore source parse
              }
            } else if (eventType === 'token') {
              try {
                const parsed = JSON.parse(eventData);
                if (parsed.token !== undefined) {
                  streamedText += parsed.token;
                }
              } catch {
                streamedText += eventData;
              }
            } else if (eventType === 'error') {
              try {
                const parsed = JSON.parse(eventData);
                streamedText += `\n[Stream Error: ${parsed.error || 'Server error'}]`;
              } catch {
                streamedText += `\n[Stream Error: ${eventData}]`;
              }
            }

            setMessages((prev) =>
              prev.map((msg) =>
                msg.id === agentMsgId
                  ? {
                      ...msg,
                      text: streamedText,
                      sources: streamedSources,
                    }
                  : msg
              )
            );
          }
        }
      } else {
        // Unary Fallback
        const data: AskResponse = await response.json();
        const agentMessage: ChatMessage = {
          id: generateId(),
          text: data.answer_text,
          sender: 'agent',
          timestamp: new Date(),
          sources: data.retrieved_sources?.length > 0 ? data.retrieved_sources : undefined,
        };

        setMessages((prev) => [...prev, agentMessage]);
      }
    } catch (err) {
      console.error('[FloatingAssistant] Query error:', err);
      const errorMsg =
        err instanceof Error ? err.message : 'Unable to connect to RAG backend. Make sure FastAPI is running on port 8000.';
      setMessages((prev) => [
        ...prev,
        {
          id: generateId(),
          text: `Notice: ${errorMsg}`,
          sender: 'system',
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }, [inputQuery, isLoading]);

  if (!isBrowser) return null;

  return (
    <>
      {/* Floating Trigger Button */}
      <button
        type="button"
        className={`${styles.floatingButton} ${isOpen ? styles.floatingButtonActive : ''}`}
        onClick={() => setIsOpen((prev) => !prev)}
        aria-label="Toggle AI Book Assistant"
        aria-expanded={isOpen}
        title="Ask AI Assistant (Ctrl+K / ⌘K)"
      >
        <span className={styles.floatingButtonGlow} />
        <div className={styles.floatingButtonIconWrapper}>
          <SparkleBotIcon />
          <span className={styles.pulseDot} />
        </div>
        <span className={styles.floatingButtonLabel}>Ask AI Tutor</span>
        <span className={styles.floatingButtonBadge}>⌘K</span>
      </button>

      {/* Backdrop overlay */}
      {isOpen && (
        <div
          className={styles.backdrop}
          onClick={() => setIsOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Slide-out Drawer */}
      <div
        className={`${styles.drawer} ${isOpen ? styles.drawerOpen : ''}`}
        role="dialog"
        aria-modal="true"
        aria-label="Physical AI & Robotics Assistant"
      >
        {/* Drawer Header */}
        <div className={styles.drawerHeader}>
          <div className={styles.headerLeft}>
            <div className={styles.botAvatar}>
              <SparkleBotIcon />
            </div>
            <div>
              <div className={styles.headerTitle}>Physical AI Tutor</div>
              <div className={styles.headerSubtitle}>
                <span className={styles.onlineBadge}>● Online</span> Grounded in 26 Chapters
              </div>
            </div>
          </div>

          <div className={styles.headerRight}>
            <button
              type="button"
              className={styles.iconButton}
              onClick={handleClear}
              title="Clear chat history"
              aria-label="Clear chat"
            >
              <TrashIcon />
            </button>
            <button
              type="button"
              className={styles.iconButton}
              onClick={() => setIsOpen(false)}
              title="Close Assistant (Esc)"
              aria-label="Close Assistant"
            >
              <CloseIcon />
            </button>
          </div>
        </div>

        {/* Message Log */}
        <div className={styles.messageList} role="log" aria-live="polite">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`${styles.messageWrapper} ${styles[msg.sender]}`}
            >
              <div className={styles.messageBubble}>
                <div className={styles.messageBubbleHeader}>
                  <span className={styles.senderLabel}>
                    {msg.sender === 'user' ? 'You' : msg.sender === 'agent' ? 'AI Robotics Tutor' : 'System'}
                  </span>
                  {msg.sender === 'agent' && (
                    <button
                      type="button"
                      className={styles.copyBtn}
                      onClick={() => handleCopy(msg.id, msg.text)}
                      title="Copy response"
                    >
                      {copiedId === msg.id ? (
                        <>
                          <CheckIcon />
                          <span>Copied</span>
                        </>
                      ) : (
                        <>
                          <CopyIcon />
                          <span>Copy</span>
                        </>
                      )}
                    </button>
                  )}
                </div>

                <div className={styles.messageText}>{msg.text}</div>

                {/* Citations */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className={styles.sourcesContainer}>
                    <span className={styles.sourcesTitle}>Chapter References:</span>
                    <div className={styles.sourcePills}>
                      {msg.sources.map((src, idx) => (
                        <a
                          key={idx}
                          href={formatSourceUrl(src)}
                          className={styles.sourcePill}
                          title={`Navigate to ${formatSourceLabel(src, idx)}`}
                        >
                          <span>{formatSourceLabel(src, idx)}</span>
                          <ExternalLinkIcon />
                        </a>
                      ))}
                    </div>
                  </div>
                )}

                <div className={styles.messageTime}>
                  {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))}

          {/* Quick Starter Prompts — Contextually Tailored to Current Module */}
          {messages.length === 1 && (
            <div className={styles.quickPromptsSection}>
              <div className={styles.quickPromptsHeader}>
                <SparklesIcon />
                <span>Contextual topics for this chapter:</span>
              </div>
              <div className={styles.promptsGrid}>
                {contextualPrompts.map((p, idx) => (
                  <button
                    key={idx}
                    type="button"
                    className={styles.promptCard}
                    onClick={() => handleSendMessage(p.query)}
                    disabled={isLoading}
                  >
                    <span className={styles.promptTag}>{p.tag}</span>
                    <span className={styles.promptText}>{p.query}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Thinking Indicator */}
          {isLoading && (
            <div className={styles.typingContainer}>
              <div className={styles.typingDots}>
                <span /><span /><span />
              </div>
              <span className={styles.typingText}>Searching vector index & synthesizing answer…</span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Drawer Footer Input */}
        <div className={styles.drawerFooter}>
          <div className={styles.inputWrapper}>
            <input
              ref={inputRef}
              type="text"
              className={styles.drawerInput}
              placeholder="Ask a technical question about any chapter..."
              value={inputQuery}
              onChange={(e) => setInputQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
              disabled={isLoading}
              maxLength={1000}
            />
            <button
              type="button"
              className={styles.sendButton}
              onClick={() => handleSendMessage()}
              disabled={isLoading || !inputQuery.trim()}
              aria-label="Send question"
            >
              <SendIcon />
            </button>
          </div>
          <div className={styles.drawerHint}>
            <span>Pro-tip: Press Enter to send, Esc to dismiss</span>
            <span>Retrieval Augmented Generation</span>
          </div>
        </div>
      </div>
    </>
  );
}
