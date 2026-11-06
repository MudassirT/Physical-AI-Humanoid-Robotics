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

type FeatureItem = {
  num: string;
  icon: ReactNode;
  title: string;
  description: ReactNode;
  bullets: string[];
  to: string;
};

const FeatureList: FeatureItem[] = [
  {
    num: '01',
    icon: <NervousSystemIcon />,
    title: 'Module 1: The Robotic Nervous System (ROS 2)',
    description: (
      <>
        Master the Robot Operating System (ROS 2) middleware layer, DDS communication,
        modular node graphs, and real-time control for humanoid hardware.
      </>
    ),
    bullets: ['Nodes & Topics', 'DDS & QoS Policies', 'Services & Actions', 'RCLPY Architecture'],
    to: '/ai-book/module1-ros2/1-1-introduction',
  },
  {
    num: '02',
    icon: <DigitalTwinIcon />,
    title: 'Module 2: The Digital Twin (Gazebo & Unity)',
    description: (
      <>
        Build physically accurate virtual replicas of bipedal humanoid robots in Gazebo
        and photorealistic rendering environments in the Unity Engine.
      </>
    ),
    bullets: ['Gazebo Physics', 'URDF & SDF Modeling', 'Sensor Simulation', 'Unity Robotics Hub'],
    to: '/ai-book/module2-digital-twin/2-1-introduction-to-digital-twins',
  },
  {
    num: '03',
    icon: <RobotBrainIcon />,
    title: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
    description: (
      <>
        Deploy hardware-accelerated perception pipelines with NVIDIA Isaac ROS, generate
        photorealistic synthetic data in Isaac Sim, and integrate Nav2 for bipedal locomotion.
      </>
    ),
    bullets: ['Isaac Sim & Synthetic Data', 'Isaac ROS Visual SLAM', 'TensorRT Inference', 'Nav2 Bipedal Planning'],
    to: '/ai-book/module3-ai-robot-brain/3-1-introduction-to-isaac-platform',
  },
  {
    num: '04',
    icon: <VLAIcon />,
    title: 'Module 4: Vision-Language-Action (VLA)',
    description: (
      <>
        Bridge natural language intent to embodied robotic actions. Integrate multimodal
        foundation models and LLM cognitive planners for voice-to-action humanoid manipulation.
      </>
    ),
    bullets: ['VLA Architecture', 'Voice-to-Action Pipeline', 'Cognitive Planning', 'Multimodal Grounding'],
    to: '/ai-book/module4-vla/4-1-introduction-to-vla-systems',
  },
];

function Feature({ num, icon, title, description, bullets, to }: FeatureItem) {
  return (
    <div className={clsx('col col--6', styles.featureCard)}>
      <div className={styles.card}>
        <div className={styles.cardHeader}>
          <span className={styles.cardBadge}>Module {num}</span>
          <div className={styles.iconBox}>
            {icon}
          </div>
        </div>

        <Heading as="h3" className={styles.cardTitle}>{title}</Heading>
        <p className={styles.cardDesc}>{description}</p>

        <ul className={styles.cardBullets}>
          {bullets.map((b) => (
            <li key={b} className={styles.cardBulletItem}>
              <BulletCheckIcon />
              <span>{b}</span>
            </li>
          ))}
        </ul>

        <div className={styles.cardFooter}>
          <Link className={styles.cardLink} to={to}>
            Explore Module {num} →
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
        <Heading as="h2" className={styles.sectionTitle}>
          Curriculum Modules
        </Heading>
        <p className={styles.sectionSubtitle}>
          Four comprehensive engineering units designed to transition your skills from robotics fundamentals to autonomous embodied AI.
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
