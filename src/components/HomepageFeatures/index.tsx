import React, { useState, useMemo, type ReactNode } from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import Link from '@docusaurus/Link';

// ---------------------------------------------------------------------------
// Precision Vector Icons for All 12 Modules
// ---------------------------------------------------------------------------

function NervousSystemIcon() {
  return (
    <svg className={styles.cardIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
    </svg>
  );
}

function DigitalTwinIcon() {
  return (
    <svg className={styles.cardIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3z" />
      <path d="M12 12l8-4.5" />
      <path d="M12 12v9" />
      <path d="M12 12L4 7.5" />
    </svg>
  );
}

function RobotBrainIcon() {
  return (
    <svg className={styles.cardIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="4" y="4" width="16" height="16" rx="2" />
      <rect x="9" y="9" width="6" height="6" />
      <path d="M9 1v3" />
      <path d="M15 1v3" />
      <path d="M9 20v3" />
      <path d="M15 20v3" />
      <path d="M20 9h3" />
      <path d="M20 14h3" />
      <path d="M1 9h3" />
      <path d="M1 14h3" />
    </svg>
  );
}

function VLAIcon() {
  return (
    <svg className={styles.cardIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="3" />
      <path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7Z" />
      <path d="m19 5 2-2" />
      <path d="m19 19 2 2" />
    </svg>
  );
}

function KinematicsIcon() {
  return (
    <svg className={styles.cardIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="6" cy="6" r="3" />
      <circle cx="18" cy="18" r="3" />
      <circle cx="18" cy="6" r="2" />
      <line x1="8.5" y1="7.5" x2="16" y2="16" />
      <line x1="8" y1="6" x2="16" y2="6" />
    </svg>
  );
}

function LocomotionIcon() {
  return (
    <svg className={styles.cardIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M4 22l4-8 4 3 4-9" />
      <circle cx="17" cy="4" r="2" />
      <path d="M14 10l5 3 2 7" />
    </svg>
  );
}

function ManipulationIcon() {
  return (
    <svg className={styles.cardIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M18 11V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v4" />
      <path d="M14 10V4a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v7" />
      <path d="M10 10.5V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v8" />
      <path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15" />
    </svg>
  );
}

function LearningIcon() {
  return (
    <svg className={styles.cardIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
      <circle cx="12" cy="12" r="3" />
      <line x1="12" y1="9" x2="12" y2="3" />
      <line x1="14.5" y1="13.5" x2="20" y2="16.5" />
      <line x1="9.5" y1="13.5" x2="4" y2="16.5" />
    </svg>
  );
}

function SimToRealIcon() {
  return (
    <svg className={styles.cardIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="7" cy="12" r="5" />
      <circle cx="17" cy="12" r="5" strokeDasharray="3 3" />
      <path d="M10 12h4" />
      <path d="m12 10 2 2-2 2" />
    </svg>
  );
}

function HardwareIcon() {
  return (
    <svg className={styles.cardIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
    </svg>
  );
}

function SafetyIcon() {
  return (
    <svg className={styles.cardIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
      <path d="m9 12 2 2 4-4" />
    </svg>
  );
}

function CapstoneIcon() {
  return (
    <svg className={styles.cardIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
    </svg>
  );
}

function BulletCheckIcon() {
  return (
    <svg className={styles.bulletCheck} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 0 1 .143 1.052l-8 10.5a.75.75 0 0 1-1.127.075l-4.5-4.5a.75.75 0 0 1 1.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 0 1 1.05-.143Z" clipRule="evenodd" />
    </svg>
  );
}

function ClockIcon() {
  return (
    <svg className={styles.metaIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="10" />
      <polyline points="12 6 12 12 16 14" />
    </svg>
  );
}

function ArrowRightIcon() {
  return (
    <svg className={styles.arrowIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M5 12h14" />
      <path d="m12 5 7 7-7 7" />
    </svg>
  );
}

function SearchIcon() {
  return (
    <svg className={styles.searchIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="11" cy="11" r="8" />
      <path d="m21 21-4.3-4.3" />
    </svg>
  );
}

function ClearIcon() {
  return (
    <svg className={styles.clearSearchIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M18 6 6 18" />
      <path d="m6 6 12 12" />
    </svg>
  );
}

// ---------------------------------------------------------------------------
// Curriculum Data Model — All 12 Modules
// ---------------------------------------------------------------------------

type ModuleCategory = 'all' | 'foundations' | 'embodied' | 'learning' | 'systems';

type FeatureItem = {
  num: string;
  category: ModuleCategory;
  themeClass: string;
  level: string;
  duration: string;
  icon: ReactNode;
  title: string;
  description: string;
  bullets: string[];
  to: string;
};

const FeatureList: FeatureItem[] = [
  {
    num: '01',
    category: 'foundations',
    themeClass: styles.modTheme1,
    level: 'LEVEL 1 • MIDDLEWARE',
    duration: '3.5 Hrs',
    icon: <NervousSystemIcon />,
    title: 'The Robotic Nervous System (ROS 2)',
    description: 'Master the deterministic middleware layer, DDS QoS policies, real-time lifecycle nodes, and zero-copy IPC designed for sub-millisecond humanoid joint motor commutation.',
    bullets: ['Deterministic DDS & QoS Policies', 'Iceoryx Shared Memory IPC', 'Services, Actions & Parameters', 'rclpy & rclcpp Architecture'],
    to: '/ai-book/module1-ros2/1-1-introduction',
  },
  {
    num: '02',
    category: 'foundations',
    themeClass: styles.modTheme2,
    level: 'LEVEL 2 • SIMULATION',
    duration: '4.0 Hrs',
    icon: <DigitalTwinIcon />,
    title: 'The Digital Twin (Gazebo & Unity)',
    description: 'Build high-fidelity physics replicas in Gazebo Harmonic and photorealistic sensor rendering in Unity HDRP to close the sim-to-real gap before deploying to physical robot hardware.',
    bullets: ['Rigid-Body & Multi-Contact Physics', 'URDF, Xacro & SDF Modeling', 'IMU & Stereo Camera Sensor Sim', 'Unity Robotics Hub & ROS TCP'],
    to: '/ai-book/module2-digital-twin/2-1-introduction-to-digital-twins',
  },
  {
    num: '03',
    category: 'foundations',
    themeClass: styles.modTheme3,
    level: 'LEVEL 3 • PERCEPTION',
    duration: '4.5 Hrs',
    icon: <RobotBrainIcon />,
    title: 'The AI-Robot Brain (NVIDIA Isaac)',
    description: 'Harness GPU-accelerated Isaac ROS, TensorRT perception pipelines, photorealistic synthetic data generation in Isaac Sim, and Nav2 footstep lattice planning for bipedal traversal.',
    bullets: ['Isaac Sim & Synthetic Data Generation', 'NITROS Zero-Copy Pipelines', 'cuVSLAM Visual-Inertial Odometry', 'Nav2 Bipedal Footstep Lattice'],
    to: '/ai-book/module3-ai-robot-brain/3-1-introduction-to-isaac-platform',
  },
  {
    num: '04',
    category: 'embodied',
    themeClass: styles.modTheme4,
    level: 'LEVEL 4 • EMBODIED COGNITION',
    duration: '5.0 Hrs',
    icon: <VLAIcon />,
    title: 'Vision-Language-Action (VLA) Systems',
    description: 'Bridge natural language intent to embodied robotic actions. Integrate multimodal foundation models, Whisper voice pipelines, and LLM hierarchical planners for autonomous humanoid tasks.',
    bullets: ['End-to-End VLA Architectures (OpenVLA)', 'Whisper Voice-to-Action Pipeline', 'LLM Hierarchical Cognitive Planning', '3D Affordance & Spatial Grounding'],
    to: '/ai-book/module4-vla/4-1-introduction-to-vla-systems',
  },
  {
    num: '05',
    category: 'embodied',
    themeClass: styles.modTheme5,
    level: 'LEVEL 5 • KINEMATICS & DYNAMICS',
    duration: '4.0 Hrs',
    icon: <KinematicsIcon />,
    title: 'Humanoid Kinematics & Dynamics',
    description: 'Formulate Lie group kinematics using Product of Exponentials (PoE), solve redundant inverse kinematics via null-space projection, and implement Featherstone O(n) recursive dynamics.',
    bullets: ['Product of Exponentials (PoE) & Lie Groups', 'Null-Space Redundancy Resolution', 'Featherstone Recursive Newton-Euler', 'Articulated Body Algorithm O(n)'],
    to: '/ai-book/module5-kinematics-dynamics/5-1-introduction-to-robot-kinematics',
  },
  {
    num: '06',
    category: 'embodied',
    themeClass: styles.modTheme6,
    level: 'LEVEL 6 • BIPEDAL LOCOMOTION',
    duration: '4.5 Hrs',
    icon: <LocomotionIcon />,
    title: 'Bipedal Locomotion & Whole-Body Control',
    description: 'Engineer dynamic humanoid walking cycles with the 3D Linear Inverted Pendulum Model (3D-LIPM), Kajita ZMP preview control, Divergent Component of Motion (DCM), and QP whole-body controllers.',
    bullets: ['3D-LIPM & Kajita ZMP Preview Control', 'Capture Point & DCM Footstep Adjustment', 'Quadratic Programming (QP) Whole-Body Control', 'Contact Wrenches & Foot Force Sensors'],
    to: '/ai-book/module6-bipedal-locomotion/6-1-introduction-to-bipedal-locomotion',
  },
  {
    num: '07',
    category: 'learning',
    themeClass: styles.modTheme7,
    level: 'LEVEL 7 • DEXTEROUS MANIPULATION',
    duration: '3.5 Hrs',
    icon: <ManipulationIcon />,
    title: 'Dexterous Manipulation & Hand Design',
    description: 'Design multi-fingered humanoid hands, evaluate force-closure and form-closure grasp metrics, integrate optical tactile sensors, and program in-hand reorientation policies.',
    bullets: ['Underactuated & Tendon-Driven Mechanics', 'Force-Closure Grasp Wrench Space', 'GelSight Optical Tactile Feedback', 'In-Hand Manipulation Trajectories'],
    to: '/ai-book/module7-dexterous-manipulation/7-1-introduction-to-dexterous-manipulation',
  },
  {
    num: '08',
    category: 'learning',
    themeClass: styles.modTheme8,
    level: 'LEVEL 8 • REINFORCEMENT LEARNING',
    duration: '4.5 Hrs',
    icon: <LearningIcon />,
    title: 'Robot Learning & Reinforcement Learning',
    description: 'Train robust locomotion and manipulation policies using Massively Parallel Isaac Gym simulations, PPO with Generalized Advantage Estimation, and Diffusion Policy imitation learning.',
    bullets: ['Massively Parallel Sim (Isaac Gym / Orbit)', 'PPO & Generalized Advantage Estimation', 'Diffusion Policies for Visuomotor Control', 'Curriculum Learning for Rough Terrain'],
    to: '/ai-book/module8-robot-learning/8-1-foundations-of-reinforcement-learning',
  },
  {
    num: '09',
    category: 'learning',
    themeClass: styles.modTheme9,
    level: 'LEVEL 9 • SIM-TO-REAL TRANSFER',
    duration: '3.5 Hrs',
    icon: <SimToRealIcon />,
    title: 'Sim-to-Real Transfer & Randomization',
    description: 'Eliminate sim-to-real divergence through systematic dynamics domain randomization, visual augmentation, actuator latency delay modeling, and real-time system identification.',
    bullets: ['Visual & Photometric Domain Randomization', 'Inertial, Friction & Actuator Delay Perturbations', 'Hardware System Identification (SysID)', 'Privileged Teacher-Student Distillation'],
    to: '/ai-book/module9-sim-to-real/9-1-the-reality-gap',
  },
  {
    num: '10',
    category: 'systems',
    themeClass: styles.modTheme10,
    level: 'LEVEL 10 • HARDWARE & EMBEDDED',
    duration: '4.0 Hrs',
    icon: <HardwareIcon />,
    title: 'Hardware Architecture & Embedded Systems',
    description: 'Select frameless BLDC motors, quasi-direct drive (QDD) planetary gears, EtherCAT real-time fieldbuses, power distribution architectures, and thermal management for bipedal robots.',
    bullets: ['Quasi-Direct Drive (QDD) Actuator Design', 'EtherCAT & CAN-FD Real-Time Fieldbuses', 'High-Discharge BMS & Power Budgets', 'Embedded Real-Time Linux (PREEMPT_RT)'],
    to: '/ai-book/module10-hardware-architecture/10-1-humanoid-mechanical-design',
  },
  {
    num: '11',
    category: 'systems',
    themeClass: styles.modTheme11,
    level: 'LEVEL 11 • SAFETY & ETHICS',
    duration: '3.0 Hrs',
    icon: <SafetyIcon />,
    title: 'Safety, Ethics & Humanoid Deployment',
    description: 'Implement ISO 13849 & ISO 10218 safety standards, hardware emergency stops (E-stop), torque-limiting collision detection, and ethical human-robot coexistence guidelines.',
    bullets: ['ISO 13849 & ISO 10218 Humanoid Standards', 'Torque-Limiting Safe Contact Observer', 'Hardware Safety Relay & Watchdog Architecture', 'Ethical Autonomy & Human Collaboration'],
    to: '/ai-book/module11-safety-ethics/11-1-robot-safety-standards',
  },
  {
    num: '12',
    category: 'systems',
    themeClass: styles.modTheme12,
    level: 'LEVEL 12 • CAPSTONES & FRONTIERS',
    duration: '5.0 Hrs',
    icon: <CapstoneIcon />,
    title: 'Capstone Projects & Research Frontiers',
    description: 'Integrate all layers into production capstone systems: autonomous grocery navigation, bipedal stair climbing, and open-vocabulary warehouse sorting using foundation agents.',
    bullets: ['Full-Stack Bipedal Humanoid Pipeline', 'Sim-to-Real Deployment Benchmark', 'Foundation Model Agent Orchestration', 'Research Papers & Frontier Open Issues'],
    to: '/ai-book/module12-capstone-frontiers/12-1-capstone-project-guide',
  },
];

function Feature({ num, themeClass, level, duration, icon, title, description, bullets, to }: FeatureItem) {
  return (
    <div className={clsx('col col--6 col--lg-4', styles.featureCol)}>
      <div className={clsx(styles.card, themeClass)}>
        {/* Top Meta Bar */}
        <div className={styles.cardHeader}>
          <div className={styles.headerBadges}>
            <span className={styles.cardBadge}>Module {num}</span>
            <span className={styles.levelBadge}>{level}</span>
          </div>
          <div className={styles.durationBadge}>
            <ClockIcon />
            <span>{duration}</span>
          </div>
        </div>

        {/* Icon & Title */}
        <div className={styles.titleRow}>
          <div className={styles.iconBox}>
            {icon}
          </div>
          <Heading as="h3" className={styles.cardTitle}>{title}</Heading>
        </div>

        <p className={styles.cardDesc}>{description}</p>

        {/* Key Pillars Checklist */}
        <ul className={styles.cardBullets}>
          {bullets.map((b) => (
            <li key={b} className={styles.cardBulletItem}>
              <BulletCheckIcon />
              <span>{b}</span>
            </li>
          ))}
        </ul>

        {/* Action Link */}
        <div className={styles.cardFooter}>
          <Link className={styles.cardLink} to={to}>
            <span>Explore Module {num}</span>
            <ArrowRightIcon />
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  const [selectedCategory, setSelectedCategory] = useState<ModuleCategory>('all');
  const [searchQuery, setSearchQuery] = useState('');

  const filteredFeatures = useMemo(() => {
    return FeatureList.filter((item) => {
      const matchesCategory = selectedCategory === 'all' || item.category === selectedCategory;
      if (!matchesCategory) return false;
      if (!searchQuery.trim()) return true;

      const q = searchQuery.toLowerCase().trim();
      return (
        item.title.toLowerCase().includes(q) ||
        item.description.toLowerCase().includes(q) ||
        item.level.toLowerCase().includes(q) ||
        item.bullets.some((b) => b.toLowerCase().includes(q))
      );
    });
  }, [selectedCategory, searchQuery]);

  return (
    <section id="curriculum-modules" className={styles.features}>
      <div className="container">
        {/* Section Pill */}
        <div className={styles.sectionBadgeWrapper}>
          <div className={styles.sectionBadge}>
            <span className={styles.sectionBadgeDot} />
            12-MODULE EMBODIED AI CURRICULUM
          </div>
        </div>

        <Heading as="h2" className={styles.sectionTitle}>
          Comprehensive Physical AI Engineering Pathway
        </Heading>
        <p className={styles.sectionSubtitle}>
          An end-to-end engineering journey transitioning your capabilities from sub-millisecond motor communication to autonomous multimodal humanoid behavior.
        </p>

        {/* Search & Filter Control Bar */}
        <div className={styles.controlsWrapper}>
          {/* Category Filter Pills */}
          <div className={styles.categoryFilterBar}>
            <button
              type="button"
              className={clsx(styles.filterBtn, selectedCategory === 'all' && styles.filterBtnActive)}
              onClick={() => setSelectedCategory('all')}
            >
              All 12 Modules
            </button>
            <button
              type="button"
              className={clsx(styles.filterBtn, selectedCategory === 'foundations' && styles.filterBtnActive)}
              onClick={() => setSelectedCategory('foundations')}
            >
              Phase 1: Foundations & Sim (1–3)
            </button>
            <button
              type="button"
              className={clsx(styles.filterBtn, selectedCategory === 'embodied' && styles.filterBtnActive)}
              onClick={() => setSelectedCategory('embodied')}
            >
              Phase 2: Embodied AI & VLA (4–6)
            </button>
            <button
              type="button"
              className={clsx(styles.filterBtn, selectedCategory === 'learning' && styles.filterBtnActive)}
              onClick={() => setSelectedCategory('learning')}
            >
              Phase 3: Dynamics & Learning (7–9)
            </button>
            <button
              type="button"
              className={clsx(styles.filterBtn, selectedCategory === 'systems' && styles.filterBtnActive)}
              onClick={() => setSelectedCategory('systems')}
            >
              Phase 4: Hardware & Frontiers (10–12)
            </button>
          </div>

          {/* Interactive Search Box */}
          <div className={styles.searchBarContainer}>
            <div className={styles.searchBox}>
              <SearchIcon />
              <input
                type="text"
                className={styles.searchInput}
                placeholder="Search modules (e.g. ROS 2, Isaac, VLA, MPC, EtherCAT)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                aria-label="Filter modules"
              />
              {searchQuery && (
                <button
                  type="button"
                  className={styles.clearSearchBtn}
                  onClick={() => setSearchQuery('')}
                  title="Clear search"
                >
                  <ClearIcon />
                </button>
              )}
            </div>
            <div className={styles.resultsBadge}>
              Showing <strong>{filteredFeatures.length}</strong> of 12 Modules
            </div>
          </div>
        </div>

        {/* Modules Grid */}
        {filteredFeatures.length > 0 ? (
          <div className="row">
            {filteredFeatures.map((props) => (
              <Feature key={props.num} {...props} />
            ))}
          </div>
        ) : (
          <div className={styles.emptyState}>
            <p className={styles.emptyStateTitle}>No modules match "{searchQuery}"</p>
            <p className={styles.emptyStateSub}>Try searching for "ROS 2", "Isaac", "VLA", "Locomotion", or "Reinforcement".</p>
            <button
              type="button"
              className="button button--secondary button--sm"
              onClick={() => { setSearchQuery(''); setSelectedCategory('all'); }}
            >
              Reset Filters
            </button>
          </div>
        )}
      </div>
    </section>
  );
}
