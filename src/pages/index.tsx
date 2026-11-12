import React, { useState, type ReactNode } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';
import ChatWidget from '@site/src/components/ChatWidget/ChatWidget';

import styles from './index.module.css';

// ---------------------------------------------------------------------------
// Precision Vector Icons
// ---------------------------------------------------------------------------

function ArrowRightIcon() {
  return (
    <svg className={styles.btnIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M5 12h14" />
      <path d="m12 5 7 7-7 7" />
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

function BookOpenIcon() {
  return (
    <svg className={styles.stepIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
      <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
    </svg>
  );
}

function SimulationIcon() {
  return (
    <svg className={styles.stepIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
      <polyline points="3.29 7 12 12 20.71 7" />
      <line x1="12" y1="22" x2="12" y2="12" />
    </svg>
  );
}

function PerceptionIcon() {
  return (
    <svg className={styles.stepIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="3" />
      <path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7Z" />
    </svg>
  );
}

function BrainAIIcon() {
  return (
    <svg className={styles.stepIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 2a4 4 0 0 0-4 4v2a4 4 0 0 0-2 3.46V14a4 4 0 0 0 2 3.46V18a4 4 0 0 0 4 4h0a4 4 0 0 0 4-4v-.54A4 4 0 0 0 18 14v-2.54A4 4 0 0 0 16 8V6a4 4 0 0 0-4-4z" />
      <path d="M9 12h6" />
      <path d="M12 9v6" />
    </svg>
  );
}

function RobotHeadIcon() {
  return (
    <svg className={styles.btnIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="11" width="18" height="10" rx="2" />
      <circle cx="12" cy="5" r="2" />
      <path d="M12 7v4" />
      <line x1="8" y1="16" x2="8" y2="16" />
      <line x1="16" y1="16" x2="16" y2="16" />
    </svg>
  );
}

function SparklesIcon() {
  return (
    <svg className={styles.badgeSparkle} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" />
    </svg>
  );
}

// ---------------------------------------------------------------------------
// Interactive Robotics Telemetry Showcase
// ---------------------------------------------------------------------------

const SHOWCASE_TABS = [
  {
    id: 'ros2',
    label: 'ROS 2 Middleware',
    badge: '1 kHz RT Loop',
    lang: 'C++',
    code: `// ros2_control Real-Time Joint Commutation (Module 1)
auto qos = rclcpp::QoS(10).reliability(RMW_QOS_POLICY_RELIABILITY_RELIABLE)
                         .durability(RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL);
joint_state_pub_ = this->create_publisher<sensor_msgs::msg::JointState>(
    "/humanoid/joint_states", qos);
// Zero-copy Shared Memory transport enabled via Eclipse Iceoryx
iceoryx_node.enable_zero_copy_ipc();`,
  },
  {
    id: 'sim',
    label: 'Gazebo & Unity Sim',
    badge: 'Multi-Contact DART',
    lang: 'XML / SDF',
    code: `<!-- Gazebo Harmonic Bipedal Collision & Actuator (Module 2) -->
<link name="biped_left_foot">
  <inertial mass="1.45"><inertia ixx="0.002" iyy="0.004" izz="0.003"/></inertial>
  <collision name="sole_collision">
    <surface><friction><ode mu="1.2" mu2="0.9"/></friction></surface>
  </collision>
</link>
<!-- Photorealistic Raytracing stream synced to Unity HDRP via TCP-Connector -->`,
  },
  {
    id: 'isaac',
    label: 'NVIDIA Isaac Perception',
    badge: 'NITROS Accelerated',
    lang: 'Python',
    code: `# Isaac ROS Visual SLAM & Stereo Depth (Module 3)
cuvslam_node = ComposableNode(
    package='isaac_ros_visual_slam',
    plugin='nvidia::isaac_ros::visual_slam::VisualSlamNode',
    parameters=[{'enable_rectified_pose': True, 'denoise_input_images': True}],
    remappings=[('stereo_camera/left/image', '/camera/left/image_rect_color')]
)
# NITROS zero-copy GPU memory exchange initialized at 60 FPS`,
  },
  {
    id: 'vla',
    label: 'VLA & Whole-Body Control',
    badge: 'Octo & OpenVLA',
    lang: 'Python',
    code: `# Multimodal Voice-to-Action Chunking (Module 4)
voice_instruction = whisper.transcribe(audio_stream) # "Clear the obstacle"
prompt = f"Incline: 12 deg. Obstacle at x=1.4m. Intent: {voice_instruction}"
action_chunk = vla_model.predict(rgb_front, prompt, horizon=16)
# Publish continuous 50 Hz trajectory to Nav2 & Kajita 3D-LIPM planner`,
  },
];

function RoboticsShowcase() {
  const [activeTab, setActiveTab] = useState(0);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    try {
      navigator.clipboard.writeText(SHOWCASE_TABS[activeTab].code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {}
  };

  return (
    <div className={styles.showcaseWrapper}>
      <div className={styles.showcaseHeader}>
        <div className={styles.macDots}>
          <span className={styles.dotRed} />
          <span className={styles.dotYellow} />
          <span className={styles.dotGreen} />
          <span className={styles.terminalLabel}>telemetry.ros2_node.cpp</span>
        </div>
        <div className={styles.showcaseTabs}>
          {SHOWCASE_TABS.map((tab, idx) => (
            <button
              key={tab.id}
              type="button"
              className={clsx(styles.showcaseTabBtn, activeTab === idx && styles.showcaseTabActive)}
              onClick={() => setActiveTab(idx)}
            >
              <span>{tab.label}</span>
              <span className={styles.tabPill}>{tab.badge}</span>
            </button>
          ))}
        </div>
        <button
          type="button"
          className={styles.copyBtn}
          onClick={handleCopy}
          title="Copy snippet"
        >
          {copied ? <CheckIcon /> : <CopyIcon />}
          <span>{copied ? 'Copied' : 'Copy'}</span>
        </button>
      </div>

      <div className={styles.showcaseBody}>
        <div className={styles.codeMeta}>
          <span className={styles.codeLangBadge}>{SHOWCASE_TABS[activeTab].lang}</span>
          <span className={styles.codeStateBadge}>Live Pipeline Verified</span>
        </div>
        <pre className={styles.showcaseCode}>
          <code>{SHOWCASE_TABS[activeTab].code}</code>
        </pre>
      </div>

      <div className={styles.showcaseFooter}>
        <div className={styles.showcaseStatus}>
          <span className={styles.statusGlow} />
          <span>Loop Latency: <strong>0.38 ms</strong> • Zero-Copy Iceoryx • Jitter: <strong>±0.024 ms</strong> • NOMINAL</span>
        </div>
        <Link to="/ai-book/intro" className={styles.showcaseExploreLink}>
          View Architecture Docs →
        </Link>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Hero Section
// ---------------------------------------------------------------------------

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();

  const handleScrollToModules = () => {
    document.getElementById('curriculum-modules')?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleScrollToAssistant = () => {
    document.getElementById('ai-assistant')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      {/* Dynamic Ambient Background Glow Elements */}
      <div className={styles.ambientGlowOrb1} />
      <div className={styles.ambientGlowOrb2} />
      <div className={styles.ambientGlowOrb3} />

      <div className="container">
        {/* Announcement Pill Badge */}
        <div className={styles.heroBadge}>
          <span className={styles.heroBadgeDot} />
          <SparklesIcon />
          <span>Physical AI Embodied Intelligence • 12 Industry Modules • Open Access</span>
        </div>

        {/* Title */}
        <Heading as="h1" className={clsx('hero__title', styles.heroTitle)}>
          {siteConfig.title}
        </Heading>

        {/* Subtitle */}
        <p className={clsx('hero__subtitle', styles.heroSubtitle)}>
          Master low-latency ROS 2 middleware, physics-accurate Digital Twins, NVIDIA Isaac perception,
          and Vision-Language-Action (VLA) foundation models for autonomous bipedal humanoids.
        </p>

        {/* Action Buttons */}
        <div className={styles.buttons}>
          <Link
            className="button button--primary button--lg"
            to="/ai-book/intro"
          >
            <span>Start Curriculum</span>
            <ArrowRightIcon />
          </Link>
          <button
            type="button"
            className="button button--secondary button--lg"
            onClick={handleScrollToModules}
          >
            <span>Explore 12 Modules</span>
          </button>
          <button
            type="button"
            className="button button--secondary button--lg"
            onClick={handleScrollToAssistant}
          >
            <RobotHeadIcon />
            <span>AI Robotics Tutor</span>
          </button>
        </div>

        {/* Interactive Showcase Preview */}
        <RoboticsShowcase />

        {/* Stats Strip */}
        <div className={styles.heroStats}>
          <div className={styles.heroStat}>
            <span className={styles.heroStatNumber}>12</span>
            <span className={styles.heroStatLabel}>Core Engineering Modules</span>
          </div>
          <div className={styles.heroStat}>
            <span className={styles.heroStatNumber}>26</span>
            <span className={styles.heroStatLabel}>Peer-Reviewed Chapters</span>
          </div>
          <div className={styles.heroStat}>
            <span className={styles.heroStatNumber}>1 kHz</span>
            <span className={styles.heroStatLabel}>Sub-ms Real-Time Control Loop</span>
          </div>
          <div className={styles.heroStat}>
            <span className={styles.heroStatNumber}>100%</span>
            <span className={styles.heroStatLabel}>Qdrant Grounded RAG Assistant</span>
          </div>
        </div>
      </div>
    </header>
  );
}

// ---------------------------------------------------------------------------
// How It Works / Engineering Roadmap
// ---------------------------------------------------------------------------

function HowItWorks() {
  const steps = [
    {
      icon: <BookOpenIcon />,
      num: 1,
      title: 'Deterministic Middleware',
      desc: 'Architect low-latency ROS 2 nodes, zero-copy shared memory IPC (Iceoryx), and DDS QoS policies for 1 kHz motor control loops.',
      tag: 'Phase 1 • ROS 2 Core',
      link: '/ai-book/module1-ros2/1-1-introduction',
    },
    {
      icon: <SimulationIcon />,
      num: 2,
      title: 'Physics & Digital Twins',
      desc: 'Construct kinematic URDF/SDF models in Gazebo Harmonic with multi-contact friction, and render photorealistic sensors in Unity HDRP.',
      tag: 'Phase 1 • Simulation',
      link: '/ai-book/module2-digital-twin/2-1-introduction-to-digital-twins',
    },
    {
      icon: <PerceptionIcon />,
      num: 3,
      title: 'Accelerated Perception & SLAM',
      desc: 'Deploy GPU-accelerated cuVSLAM odometry, TensorRT inference, and Nav2 bipedal footstep lattice planning in NVIDIA Isaac Sim.',
      tag: 'Phase 2 • Isaac Platform',
      link: '/ai-book/module3-ai-robot-brain/3-1-introduction-to-isaac-platform',
    },
    {
      icon: <BrainAIIcon />,
      num: 4,
      title: 'Embodied Vision-Language-Action',
      desc: 'Ground multimodal foundation models (OpenVLA, π0) to physical actions with voice-to-action translation and cognitive planners.',
      tag: 'Phase 2 • VLA Models',
      link: '/ai-book/module4-vla/4-1-introduction-to-vla-systems',
    },
  ];

  return (
    <section className={styles.howSection}>
      <div className="container">
        <div className={styles.sectionBadgeWrapper}>
          <span className={styles.sectionBadge}>ENGINEERING METHODOLOGY</span>
        </div>
        <Heading as="h2" className={styles.sectionTitle}>
          Progressive Robotics Architecture Roadmap
        </Heading>
        <p className={styles.sectionSubtitle}>
          A systematic curriculum taking engineers from sub-millisecond hardware motor commutation to high-level autonomous multimodal humanoid behavior.
        </p>

        <div className={styles.stepsGrid}>
          {steps.map((s) => (
            <Link key={s.num} to={s.link} className={styles.stepCardLink}>
              <div className={styles.stepCard}>
                <div className={styles.stepHeader}>
                  <div className={styles.stepIconWrapper}>
                    {s.icon}
                  </div>
                  <span className={styles.stepNumber}>Step 0{s.num}</span>
                </div>
                <span className={styles.stepTag}>{s.tag}</span>
                <div className={styles.stepTitle}>{s.title}</div>
                <p className={styles.stepDesc}>{s.desc}</p>
                <div className={styles.stepExplore}>Read Chapter Overview →</div>
              </div>
            </Link>
          ))}
        </div>

        {/* Tech Stack Bar */}
        <div className={styles.techStackBar}>
          <span className={styles.techStackLabel}>Technology Stack:</span>
          <div className={styles.techPills}>
            <span className={styles.techPill}>ROS 2 Humble / Iron</span>
            <span className={styles.techPill}>CycloneDDS & Iceoryx</span>
            <span className={styles.techPill}>Gazebo Harmonic</span>
            <span className={styles.techPill}>Unity HDRP</span>
            <span className={styles.techPill}>NVIDIA Isaac Sim 4.0</span>
            <span className={styles.techPill}>cuVSLAM & Nav2</span>
            <span className={styles.techPill}>OpenVLA & π0</span>
            <span className={styles.techPill}>Kajita 3D-LIPM</span>
            <span className={styles.techPill}>Qdrant Vector DB</span>
            <span className={styles.techPill}>FastAPI Backend</span>
          </div>
        </div>
      </div>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Home Page
// ---------------------------------------------------------------------------

export default function Home(): ReactNode {
  return (
    <Layout
      title="Physical AI & Humanoid Robotics Curriculum"
      description="The definitive open-access guide to Physical AI, ROS 2, Digital Twins, NVIDIA Isaac, and Vision-Language-Action systems.">
      <HomepageHeader />
      <main>
        {/* All 12 Curriculum Modules */}
        <HomepageFeatures />

        {/* Systematic Engineering Roadmap */}
        <HowItWorks />

        {/* AI Chat Assistant Section */}
        <section id="ai-assistant" className={styles.chatSection}>
          <div className="container">
            <div className={styles.sectionBadgeWrapper}>
              <span className={styles.sectionBadge}>GROUNDED EMBODIED AI</span>
            </div>
            <Heading as="h2" className={styles.chatSectionTitle}>
              Interactive AI Robotics Assistant
            </Heading>
            <p className={styles.chatSectionSubtitle}>
              Ask complex robotics questions, debug ROS 2 pipelines, or explore VLA equations.
              Grounded via Qdrant retrieval-augmented generation across all 26 chapters.
            </p>
            <ChatWidget />
          </div>
        </section>
      </main>
    </Layout>
  );
}
