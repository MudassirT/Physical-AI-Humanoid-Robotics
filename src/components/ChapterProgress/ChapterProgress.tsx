import React, { useState, useEffect, useCallback } from 'react';
import useIsBrowser from '@docusaurus/useIsBrowser';
import styles from './styles.module.css';

export interface ChapterProgressProps {
  chapterId?: string;
  moduleId?: string;
  totalChapters?: number;
}

const STORAGE_KEY = 'robotics_chapter_progress';

function getBackendUrl(): string {
  if (typeof process !== 'undefined' && process.env && process.env.REACT_APP_FASTAPI_BASE_URL) {
    return process.env.REACT_APP_FASTAPI_BASE_URL;
  }
  return 'http://127.0.0.1:8000';
}

function normalizeModuleId(chapterId?: string, explicitModuleId?: string): string {
  if (explicitModuleId) return explicitModuleId;
  if (!chapterId) return 'general';
  const match = chapterId.match(/^(\d+)-/);
  if (match) return `module${match[1]}`;
  const prefixMatch = chapterId.match(/^(module\d+)/i);
  if (prefixMatch) return prefixMatch[1].toLowerCase();
  return 'general';
}

export function ChapterProgress({
  chapterId,
  moduleId: explicitModuleId,
  totalChapters = 10,
}: ChapterProgressProps): React.JSX.Element {
  const isBrowser = useIsBrowser();
  const moduleId = normalizeModuleId(chapterId, explicitModuleId);

  const [completed, setCompleted] = useState<boolean>(false);
  const [completedChapters, setCompletedChapters] = useState<string[]>([]);

  // Load progress from localStorage safely on client mount
  useEffect(() => {
    if (!isBrowser) return;
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed)) {
          setCompletedChapters(parsed);
          setCompleted(chapterId ? parsed.includes(chapterId) : false);
        }
      }
    } catch {
      // LocalStorage unavailable (e.g. private browsing mode)
    }
  }, [isBrowser, chapterId]);

  // Telemetry dispatch
  const sendTelemetry = useCallback((newCompleted: boolean, updatedList: string[]) => {
    if (!isBrowser || !chapterId) return;
    try {
      const backendUrl = getBackendUrl();
      fetch(`${backendUrl}/analytics`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({
          event_type: 'progress_update',
          timestamp: new Date().toISOString(),
          chapter_id: chapterId,
          module_id: moduleId,
          data: {
            completed: newCompleted,
            total_completed_chapters: updatedList.length,
          },
        }),
      }).catch(() => {
        // Telemetry failure is intentionally silent
      });
    } catch {
      // Ignore network / CORS errors
    }
  }, [isBrowser, chapterId, moduleId]);

  // Toggle chapter completion
  const handleToggle = () => {
    if (!chapterId) return;
    const nextCompleted = !completed;
    let nextList: string[];

    if (nextCompleted) {
      nextList = completedChapters.includes(chapterId)
        ? completedChapters
        : [...completedChapters, chapterId];
    } else {
      nextList = completedChapters.filter((id) => id !== chapterId);
    }

    setCompleted(nextCompleted);
    setCompletedChapters(nextList);

    if (isBrowser) {
      try {
        window.localStorage.setItem(STORAGE_KEY, JSON.stringify(nextList));
      } catch {
        // Quota exceeded or disabled
      }
    }

    sendTelemetry(nextCompleted, nextList);
  };

  // Calculate module-specific progress
  const modulePrefixNum = moduleId.replace(/\D/g, '');
  const moduleCompletedCount = completedChapters.filter((id) => {
    if (modulePrefixNum) {
      const isNumPrefix = id.startsWith(`${modulePrefixNum}-`);
      const isModulePrefix = new RegExp(`^module${modulePrefixNum}([^0-9]|$)`, 'i').test(id);
      return isNumPrefix || isModulePrefix;
    }
    return id.includes(moduleId);
  }).length;

  const validTotal = Math.max(1, totalChapters);
  const percent = Math.min(100, Math.round((moduleCompletedCount / validTotal) * 100));

  return (
    <div className={styles.progressContainer} aria-label="Chapter Progress Tracker">
      <div className={styles.headerRow}>
        <div className={styles.titleArea}>
          <div className={styles.iconWrapper} aria-hidden="true">
            {completed ? (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M20 6L9 17l-5-5" />
              </svg>
            ) : (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
              </svg>
            )}
          </div>
          <div>
            <h4 className={styles.statusTitle}>
              {completed ? 'Chapter Completed ✓' : 'Chapter In Progress'}
            </h4>
            <p className={styles.statusSubtitle}>
              {completed
                ? 'Your progress is recorded in your local curriculum state.'
                : 'Click when you have finished studying this material.'}
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={handleToggle}
          className={`${styles.toggleButton} ${
            completed ? styles.toggleButtonCompleted : styles.toggleButtonIncomplete
          }`}
          aria-pressed={completed}
        >
          {completed ? (
            <>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <polyline points="20 6 9 17 4 12" />
              </svg>
              <span>Completed ✓</span>
            </>
          ) : (
            <>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <circle cx="12" cy="12" r="9" />
                <path d="M12 8v8" />
                <path d="M8 12h8" />
              </svg>
              <span>Mark as Complete</span>
            </>
          )}
        </button>
      </div>

      <div className={styles.statsSection}>
        <div className={styles.barRow}>
          <span className={styles.barLabel}>
            Module Progress: {moduleCompletedCount} / {validTotal} Chapters
          </span>
          <span className={styles.barValue}>{percent}%</span>
        </div>
        <div className={styles.progressBarBg} role="progressbar" aria-valuenow={percent} aria-valuemin={0} aria-valuemax={100}>
          <div
            className={`${styles.progressBarFill} ${percent === 100 ? styles.progressBarFillComplete : ''}`}
            style={{ width: `${percent}%` }}
          />
        </div>
        <div className={styles.curriculumBadge}>
          <span>Total Curriculum Chapters Completed:</span>
          <span className={styles.curriculumCount}>{completedChapters.length}</span>
        </div>
      </div>
    </div>
  );
}

export default ChapterProgress;
