import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';
import ChatWidget from '@site/src/components/ChatWidget/ChatWidget';

import styles from './index.module.css';

// ---------------------------------------------------------------------------
// Hero
// ---------------------------------------------------------------------------

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        {/* Pill Badge */}
        <div className={styles.heroBadge}>
          <span className={styles.heroBadgeDot} />
          Physical AI & Humanoid Robotics Curriculum
        </div>

        {/* Title */}
        <Heading as="h1" className={clsx('hero__title', styles.heroTitle)}>
          {siteConfig.title}
        </Heading>

        {/* Subtitle */}
        <p className={clsx('hero__subtitle', styles.heroSubtitle)}>
          {siteConfig.tagline}
        </p>

        {/* CTA Buttons */}
        <div className={styles.buttons}>
          <Link
            className="button button--primary button--lg"
            to="/ai-book/intro">
            Start Reading →
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/ai-book/intro">
            Browse Curriculum
          </Link>
        </div>

        {/* Stats strip */}
        <div className={styles.heroStats}>
          <div className={styles.heroStat}>
            <span className={styles.heroStatNumber}>4</span>
            <span className={styles.heroStatLabel}>Modules</span>
          </div>
          <div className={styles.heroStat}>
            <span className={styles.heroStatNumber}>26</span>
            <span className={styles.heroStatLabel}>Chapters</span>
          </div>
          <div className={styles.heroStat}>
            <span className={styles.heroStatNumber}>RAG</span>
            <span className={styles.heroStatLabel}>AI Assistant</span>
          </div>
          <div className={styles.heroStat}>
            <span className={styles.heroStatNumber}>100%</span>
            <span className={styles.heroStatLabel}>Open Access</span>
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className={styles.scrollIndicator}>
        <span>Scroll to explore</span>
        <div className={styles.scrollArrow} />
      </div>
    </header>
  );
}

// ---------------------------------------------------------------------------
// How It Works
// ---------------------------------------------------------------------------

function HowItWorks() {
  const steps = [
    {
      icon: '📚',
      num: 1,
      title: 'Structured Curriculum',
      desc: 'Master 4 core modules covering ROS 2, Gazebo physics, Unity visualization, and Vision-Language-Action systems.',
    },
    {
      icon: '🧪',
      num: 2,
      title: 'Simulation & Digital Twins',
      desc: 'Practice safely with high-fidelity digital twins in Gazebo, Unity, and NVIDIA Isaac before real hardware deployment.',
    },
    {
      icon: '🤖',
      num: 3,
      title: 'Context-Aware AI Tutor',
      desc: 'Ask questions anytime. The embedded RAG agent retrieves exact chapter excerpts to ground every explanation with citations.',
    },
  ];

  return (
    <section className={styles.howSection}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>
          How It Works
        </Heading>
        <p className={styles.sectionSubtitle}>
          A hands-on, progressive engineering pathway from foundational robotics communication to autonomous cognitive agents.
        </p>
        <div className={styles.stepsGrid}>
          {steps.map((s) => (
            <div key={s.num} className={styles.stepCard}>
              <div className={styles.stepHeader}>
                <span className={styles.stepIcon}>{s.icon}</span>
                <span className={styles.stepNumber}>Step 0{s.num}</span>
              </div>
              <div className={styles.stepTitle}>{s.title}</div>
              <p className={styles.stepDesc}>{s.desc}</p>
            </div>
          ))}
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
      title="Home"
      description="An Introduction to Physical AI & Humanoid Robotics">
      <HomepageHeader />
      <main>
        {/* Learning modules */}
        <HomepageFeatures />

        {/* How it works */}
        <HowItWorks />

        {/* AI Chat Assistant */}
        <section className={styles.chatSection}>
          <div className="container">
            <Heading as="h2" className={styles.chatSectionTitle}>
              Interactive AI Assistant
            </Heading>
            <p className={styles.chatSectionSubtitle}>
              Ask technical questions about any chapter. Powered by retrieval-augmented generation grounded in the book.
            </p>
            <ChatWidget />
          </div>
        </section>
      </main>
    </Layout>
  );
}
