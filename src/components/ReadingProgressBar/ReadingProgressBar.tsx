import React, { useEffect, useRef } from 'react';
import styles from './styles.module.css';

/**
 * Ultra-high-performance 60 FPS Reading Progress Bar.
 * Mutates CSS transform scaleX directly on the DOM node to eliminate
 * all React component re-renders while scrolling.
 */
export default function ReadingProgressBar(): React.ReactElement {
  const barRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let ticking = false;

    const updateBar = () => {
      const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
      const totalScrollable = scrollHeight - clientHeight;

      if (barRef.current) {
        if (totalScrollable > 80) {
          const ratio = Math.min(1, Math.max(0, scrollTop / totalScrollable));
          barRef.current.style.transform = `scaleX(${ratio})`;
          barRef.current.style.opacity = ratio > 0 ? '1' : '0';
        } else {
          barRef.current.style.opacity = '0';
        }
      }
      ticking = false;
    };

    const handleScroll = () => {
      if (!ticking) {
        window.requestAnimationFrame(updateBar);
        ticking = true;
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('resize', handleScroll, { passive: true });
    updateBar();

    return () => {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', handleScroll);
    };
  }, []);

  return (
    <div className={styles.progressBarContainer} aria-hidden="true">
      <div ref={barRef} className={styles.progressBarFill} />
    </div>
  );
}
