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
// SVG Icons (Precision Vector)
// ---------------------------------------------------------------------------

function ArrowRightIcon() {
  return (
    <svg className={styles.btnIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M5 12h14" />
      <path d="m12 5 7 7-7 7" />
    </svg>
  );
}

function TerminalIcon() {
  return (
    <svg className={styles.terminalIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <polyline points="4 17 10 11 4 5" />
      <line x1="12" y1="19" x2="20" y2="19" />
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

// ---------------------------------------------------------------------------
// Interactive Robotics Telemetry Showcase
// ---------------------------------------------------------------------------

const SHOWCASE_TABS = [
  {
    id: 'ros2',
    label: 'ROS 2 Middleware',
    badge: '1 kHz Loop',
    code: `// ros2_control Real-Time Joint Commutation (Module 1)
auto qos = rclcpp::QoS(10).reliability(RMW_QOS_POLICY_RELIABILITY_RELIABLE)
                         .durability(RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL);
joint_state_pub_ = this->create_publisher<sensor_msgs::msg::JointState>(
    "/humanoid/joint_states", qos);
// Zero-copy Shared Memory transport enabled via Iceoryx`,
  },
  {
    id: 'sim',
    label: 'Gazebo & Unity Sim',
    badge: 'Multi-Contact DART',
    code: `<!-- Gazebo Harmonic Bipedal Collision & Actuator (Module 2) -->
<link name="biped_left_foot">
  <inertial mass="1.45"><inertia ixx="0.002" iyy="0.004" izz="0.003"/></inertial>
  <collision name="sole_collision">
    <surface><friction><ode mu="1.2" mu2="0.9"/></friction></surface>
  </collision>
</link>
<!-- Photorealistic Raytracing stream synced to Unity HDRP -->`,
  },
  {
    id: 'isaac',
    label: 'NVIDIA Isaac Perception',
    badge: 'NITROS Accelerated',
    code: `# Isaac ROS Visual SLAM & Stereo Depth (Module 3)
cuvslam_node = ComposableNode(
    package='isaac_ros_visual_slam',
    plugin='nvidia::isaac_ros::visual_slam::VisualSlamNode',
    parameters=[{'enable_rectified_pose': True, 'denoise_input_images': True}],
    remappings=[('stereo_camera/left/image', '/camera/left/image_rect_color')]
)`,
  },
  {
    id: 'vla',
    label: 'VLA Action Policies',
    badge: 'Octo & OpenVLA',
    code: `# Multimodal Voice-to-Action Chunking (Module 4)
voice_instruction = whisper.transcribe(audio_stream) # "Clear the obstacle"
prompt = f"Incline: 12 deg. Obstacle at x=1.4m. Intent: {voice_instruction}"
action_chunk = vla_model.predict(rgb_front, prompt, horizon=16)
# Publish continuous 50 Hz trajectory to Nav2 lattice planner`,
  },
];

function RoboticsShowcase() {
  const [activeTab, setActiveTab] = useState(0);

  return (
    <div className={styles.showcaseWrapper}>
      <div className={styles.showcaseHeader}>
        <div className={styles.macDots}>
          <span className={styles.dotRed} />
          <span className={styles.dotYellow} />
          <span className={styles.dotGreen} />
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
      </div>
      <div className={styles.showcaseBody}>
        <pre className={styles.showcaseCode}>
          <code>{SHOWCASE_TABS[activeTab].code}</code>
        </pre>
      </div>
      <div className={styles.showcaseFooter}>
        <div className={styles.showcaseStatus}>
          <span className={styles.statusGlow} />
          <span>Telemetry: 1000 Hz Hard Real-Time • End-to-End VLA Grounded</span>
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
      <div className="container">
        {/* Announcement Pill Badge */}
        <div className={styles.heroBadge}>
          <span className={styles.heroBadgeDot} />
          <span>Physical AI & Humanoid Robotics • Comprehensive Curriculum</span>
        </div>

        {/* Title */}
        <Heading as="h1" className={clsx('hero__title', styles.heroTitle)}>
          {siteConfig.title}
        </Heading>

        {/* Subtitle */}
        <p className={clsx('hero__subtitle', styles.heroSubtitle)}>
          Master low-latency ROS 2 middleware, physics-accurate Digital Twins, NVIDIA Isaac perception,
          and Vision-Language-Action foundation models for bipedal humanoid robots.
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
            <span>Browse 4 Modules</span>
          </button>
          <button
            type="button"
            className="button button--secondary button--lg"
            onClick={handleScrollToAssistant}
          >
            <span>Interactive AI Tutor</span>
          </button>
        </div>

        {/* Interactive Showcase Preview */}
        <RoboticsShowcase />

        {/* Stats Strip */}
        <div className={styles.heroStats}>
          <div className={styles.heroStat}>
            <span className={styles.heroStatNumber}>4</span>
            <span className={styles.heroStatLabel}>Core Modules</span>
          </div>
          <div className={styles.heroStat}>
            <span className={styles.heroStatNumber}>26</span>
            <span className={styles.heroStatLabel}>In-Depth Chapters</span>
          </div>
          <div className={styles.heroStat}>
            <span className={styles.heroStatNumber}>RAG</span>
            <span className={styles.heroStatLabel}>Vector AI Tutor</span>
          </div>
          <div className={styles.heroStat}>
            <span className={styles.heroStatNumber}>100%</span>
            <span className={styles.heroStatLabel}>Open Access</span>
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
      tag: 'Module 1 • ROS 2',
      link: '/ai-book/module1-ros2/1-1-introduction',
    },
    {
      icon: <SimulationIcon />,
      num: 2,
      title: 'Physics & Digital Twins',
      desc: 'Construct kinematic URDF/SDF models in Gazebo Harmonic with multi-contact friction, and render photorealistic sensors in Unity HDRP.',
      tag: 'Module 2 • Simulation',
      link: '/ai-book/module2-digital-twin/2-1-introduction-to-digital-twins',
    },
    {
      icon: <PerceptionIcon />,
      num: 3,
      title: 'Accelerated Perception & SLAM',
      desc: 'Deploy GPU-accelerated cuVSLAM odometry, TensorRT inference, and Nav2 bipedal footstep lattice planning in NVIDIA Isaac Sim.',
      tag: 'Module 3 • Isaac Platform',
      link: '/ai-book/module3-ai-robot-brain/3-1-introduction-to-isaac-platform',
    },
    {
      icon: <BrainAIIcon />,
      num: 4,
      title: 'Embodied Vision-Language-Action',
      desc: 'Ground multimodal foundation models (OpenVLA, π0) to physical actions with voice-to-action translation and cognitive planners.',
      tag: 'Module 4 • VLA Models',
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
            <span className={styles.techPill}>Qdrant Vector DB</span>
            <span className={styles.techPill}>FastAPI</span>
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
        {/* 4 Curriculum Modules */}
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
