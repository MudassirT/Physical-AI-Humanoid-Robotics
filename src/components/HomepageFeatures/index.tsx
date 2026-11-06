import type { ReactNode } from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import Link from '@docusaurus/Link';

type FeatureItem = {
  num: string;
  icon: string;
  title: string;
  description: ReactNode;
  bullets: string[];
  to: string;
};

const FeatureList: FeatureItem[] = [
  {
    num: '01',
    icon: '⚡',
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
    icon: '🌐',
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
    icon: '🧠',
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
    icon: '🤖',
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
          <span className={styles.cardIcon}>{icon}</span>
        </div>

        <Heading as="h3" className={styles.cardTitle}>{title}</Heading>
        <p className={styles.cardDesc}>{description}</p>

        <ul className={styles.cardBullets}>
          {bullets.map((b) => (
            <li key={b} className={styles.cardBulletItem}>
              {b}
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
