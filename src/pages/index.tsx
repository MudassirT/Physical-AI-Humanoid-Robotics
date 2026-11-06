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
// SVG Icons (Lucide-inspired vector precision)
// ---------------------------------------------------------------------------

function ArrowRightIcon() {
  return (
    <svg className={styles.btnIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M5 12h14" />
      <path d="m12 5 7 7-7 7" />
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
// Hero
// ---------------------------------------------------------------------------

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();

  const handleScrollToExplore = () => {
    const el = document.getElementById('curriculum-modules');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    } else {
      window.scrollTo({ top: window.innerHeight * 0.85, behavior: 'smooth' });
    }
  };

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
            <span>Start Reading</span>
            <ArrowRightIcon />
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/ai-book/intro">
            <span>Browse Curriculum</span>
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
      <button
        type="button"
        className={styles.scrollIndicator}
        onClick={handleScrollToExplore}
        aria-label="Scroll to explore curriculum modules"
      >
        <span>Scroll to explore</span>
        <div className={styles.scrollArrow} />
      </button>
    </header>
  );
}

// ---------------------------------------------------------------------------
// How It Works
// ---------------------------------------------------------------------------

function HowItWorks() {
  const steps = [
    {
      icon: <BookOpenIcon />,
      num: 1,
      title: 'Structured Curriculum',
      desc: 'Master 4 core modules covering ROS 2, Gazebo physics, Unity visualization, and Vision-Language-Action systems.',
    },
    {
      icon: <SimulationIcon />,
      num: 2,
      title: 'Simulation & Digital Twins',
      desc: 'Practice safely with high-fidelity digital twins in Gazebo, Unity, and NVIDIA Isaac before real hardware deployment.',
    },
    {
      icon: <BrainAIIcon />,
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
                <div className={styles.stepIconWrapper}>
                  {s.icon}
                </div>
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
