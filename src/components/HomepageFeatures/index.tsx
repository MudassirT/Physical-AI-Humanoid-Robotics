import type { ReactNode } from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import Link from '@docusaurus/Link';

// ---------------------------------------------------------------------------
// Module SVG Icons (Precision Vector)
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

type FeatureItem = {
  num: string;
  themeClass: string;
  level: string;
  duration: string;
  icon: ReactNode;
  title: string;
  description: ReactNode;
  bullets: string[];
  to: string;
};

const FeatureList: FeatureItem[] = [
  {
    num: '01',
    themeClass: styles.modTheme1,
    level: 'LEVEL 1 • MIDDLEWARE',
    duration: '3.5 Hrs',
    icon: <NervousSystemIcon />,
    title: 'The Robotic Nervous System (ROS 2)',
    description: (
      <>
        Master the deterministic middleware layer, DDS QoS policies, real-time lifecycle nodes,
        and zero-copy IPC designed for sub-millisecond humanoid joint motor commutation.
      </>
    ),
    bullets: ['Deterministic DDS & QoS Policies', 'Iceoryx Shared Memory IPC', 'Services, Actions & Parameters', 'rclpy & rclcpp Architecture'],
    to: '/ai-book/module1-ros2/1-1-introduction',
  },
  {
    num: '02',
    themeClass: styles.modTheme2,
    level: 'LEVEL 2 • SIMULATION',
    duration: '4.0 Hrs',
    icon: <DigitalTwinIcon />,
    title: 'The Digital Twin (Gazebo & Unity)',
    description: (
      <>
        Build high-fidelity physics replicas in Gazebo Harmonic and photorealistic sensor rendering
        in Unity HDRP to close the sim-to-real gap before deploying to physical robot hardware.
      </>
    ),
    bullets: ['Rigid-Body & Multi-Contact Physics', 'URDF, Xacro & SDF Modeling', 'IMU & Stereo Camera Sensor Sim', 'Unity Robotics Hub & ROS TCP'],
    to: '/ai-book/module2-digital-twin/2-1-introduction-to-digital-twins',
  },
  {
    num: '03',
    themeClass: styles.modTheme3,
    level: 'LEVEL 3 • PERCEPTION',
    duration: '4.5 Hrs',
    icon: <RobotBrainIcon />,
    title: 'The AI-Robot Brain (NVIDIA Isaac)',
    description: (
      <>
        Harness GPU-accelerated Isaac ROS, TensorRT perception pipelines, photorealistic synthetic
        data generation in Isaac Sim, and Nav2 footstep lattice planning for bipedal traversal.
      </>
    ),
    bullets: ['Isaac Sim & Synthetic Data Generation', 'NITROS Zero-Copy Pipelines', 'cuVSLAM Visual-Inertial Odometry', 'Nav2 Bipedal Footstep Lattice'],
    to: '/ai-book/module3-ai-robot-brain/3-1-introduction-to-isaac-platform',
  },
  {
    num: '04',
    themeClass: styles.modTheme4,
    level: 'LEVEL 4 • EMBODIED COGNITION',
    duration: '5.0 Hrs',
    icon: <VLAIcon />,
    title: 'Vision-Language-Action (VLA)',
    description: (
      <>
        Bridge natural language intent to embodied robotic actions. Integrate multimodal foundation
        models, Whisper voice pipelines, and LLM hierarchical planners for autonomous humanoid tasks.
      </>
    ),
    bullets: ['End-to-End VLA Architectures (OpenVLA)', 'Whisper Voice-to-Action Pipeline', 'LLM Hierarchical Cognitive Planning', '3D Affordance & Spatial Grounding'],
    to: '/ai-book/module4-vla/4-1-introduction-to-vla-systems',
  },
];

function Feature({ num, themeClass, level, duration, icon, title, description, bullets, to }: FeatureItem) {
  return (
    <div className={clsx('col col--6', styles.featureCol)}>
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
  return (
    <section id="curriculum-modules" className={styles.features}>
      <div className="container">
        {/* Section Pill */}
        <div className={styles.sectionBadge}>
          <span className={styles.sectionBadgeDot} />
          SYSTEMATIC ENGINEERING CURRICULUM
        </div>

        <Heading as="h2" className={styles.sectionTitle}>
          Four Pillars of Embodied Intelligence
        </Heading>
        <p className={styles.sectionSubtitle}>
          An end-to-end engineering journey transitioning your capabilities from low-level deterministic motor communication to autonomous multimodal humanoid behavior.
        </p>

        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
