import React, { useState, useEffect, useCallback } from 'react';
import useIsBrowser from '@docusaurus/useIsBrowser';
import styles from './styles.module.css';

export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correctIndex: number;
  explanation: string;
}

export interface QuizProps {
  quizId: string;
  title?: string;
  moduleId?: string;
  questions?: QuizQuestion[];
  passThreshold?: number; // e.g. 70 or 0.70
}

const STORAGE_KEY = 'robotics_quiz_scores';

function getBackendUrl(): string {
  if (typeof process !== 'undefined' && process.env && process.env.REACT_APP_FASTAPI_BASE_URL) {
    return process.env.REACT_APP_FASTAPI_BASE_URL;
  }
  return 'http://127.0.0.1:8000';
}

export function QuizEngine({
  quizId,
  title = 'Chapter Mastery Check',
  moduleId = 'general',
  questions = [],
  passThreshold = 70,
}: QuizProps): React.JSX.Element {
  const isBrowser = useIsBrowser();
  const normalizedThreshold = passThreshold <= 1 ? Math.round(passThreshold * 100) : passThreshold;

  // Defensively normalize questions and guarantee unique question IDs
  const safeQuestions = React.useMemo(() => {
    if (!Array.isArray(questions)) return [];
    const seenIds = new Set<string>();
    return questions.map((q, idx) => {
      let qId = q?.id ? String(q.id).trim() : `q-${idx}`;
      if (!qId || seenIds.has(qId)) {
        qId = `${qId || 'q'}-${idx}`;
      }
      seenIds.add(qId);
      return {
        ...q,
        id: qId,
        question: q?.question || '',
        options: Array.isArray(q?.options) ? q.options : [],
        correctIndex: typeof q?.correctIndex === 'number' ? q.correctIndex : 0,
        explanation: q?.explanation || '',
      };
    });
  }, [questions]);

  const [selectedOptions, setSelectedOptions] = useState<Record<string, number>>({});
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
  const [score, setScore] = useState<number>(0);
  const [passed, setPassed] = useState<boolean>(false);
  const [persistedRecord, setPersistedRecord] = useState<{ score: number; passed: boolean } | null>(null);

  // Load persisted quiz history from localStorage
  useEffect(() => {
    if (!isBrowser) return;
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (parsed && typeof parsed === 'object' && !Array.isArray(parsed) && parsed[quizId]) {
          setPersistedRecord(parsed[quizId]);
        }
      }
    } catch {
      // Storage unavailable
    }
  }, [isBrowser, quizId]);

  const handleSelectOption = (questionId: string, optionIndex: number) => {
    if (isSubmitted) return;
    setSelectedOptions((prev) => ({
      ...prev,
      [questionId]: optionIndex,
    }));
  };

  const answeredCount = Object.keys(selectedOptions).length;
  const isAllAnswered = safeQuestions.length > 0 && answeredCount === safeQuestions.length;

  const sendTelemetry = useCallback(
    (finalScore: number, isPassed: boolean, correctCount: number) => {
      if (!isBrowser) return;
      try {
        const backendUrl = getBackendUrl();
        fetch(`${backendUrl}/analytics`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
          },
          body: JSON.stringify({
            event_type: 'quiz_score',
            timestamp: new Date().toISOString(),
            chapter_id: quizId,
            module_id: moduleId,
            data: {
              quiz_id: quizId,
              score: finalScore,
              passed: isPassed,
              correct_count: correctCount,
              total_questions: safeQuestions.length,
            },
          }),
        }).catch(() => {
          // Telemetry fails silently
        });
      } catch {
        // Ignore network / CORS errors
      }
    },
    [isBrowser, quizId, moduleId, safeQuestions.length]
  );

  const handleSubmit = () => {
    if (!isAllAnswered || safeQuestions.length === 0) return;

    let correctCount = 0;
    safeQuestions.forEach((q) => {
      if (selectedOptions[q.id] === q.correctIndex) {
        correctCount += 1;
      }
    });

    const finalScore = Math.round((correctCount / safeQuestions.length) * 100);
    const isPassed = finalScore >= normalizedThreshold;

    setScore(finalScore);
    setPassed(isPassed);
    setIsSubmitted(true);

    if (isBrowser) {
      try {
        const raw = window.localStorage.getItem(STORAGE_KEY);
        let existing: Record<string, any> = {};
        if (raw) {
          const parsed = JSON.parse(raw);
          if (parsed && typeof parsed === 'object' && !Array.isArray(parsed)) {
            existing = parsed;
          }
        }
        existing[quizId] = {
          score: finalScore,
          passed: isPassed,
          timestamp: new Date().toISOString(),
        };
        window.localStorage.setItem(STORAGE_KEY, JSON.stringify(existing));
        setPersistedRecord(existing[quizId]);
      } catch {
        // Ignore quota/private mode errors
      }
    }

    sendTelemetry(finalScore, isPassed, correctCount);
  };

  const handleRetake = () => {
    setSelectedOptions({});
    setIsSubmitted(false);
    setScore(0);
    setPassed(false);
  };

  if (safeQuestions.length === 0) {
    return (
      <div className={styles.quizCard}>
        <p>No questions configured for this quiz.</p>
      </div>
    );
  }

  return (
    <div className={styles.quizCard} aria-label={`Quiz: ${title}`}>
      <div className={styles.quizHeader}>
        <h3 className={styles.quizTitle}>
          <span>🎯</span>
          <span>{title}</span>
        </h3>
        {moduleId && <span className={styles.badgeModule}>{moduleId}</span>}
      </div>

      {/* Submitted Score Banner */}
      {isSubmitted && (
        <div
          className={`${styles.scoreBanner} ${
            passed ? styles.scoreBannerPass : styles.scoreBannerFail
          }`}
          role="status"
          aria-live="polite"
        >
          <div className={styles.scoreIcon}>{passed ? '🎉' : '📚'}</div>
          <div>
            <p className={styles.scoreTextTitle}>
              {passed
                ? `Passed! Score: ${score}% (Threshold: ${normalizedThreshold}%)`
                : `Score: ${score}% — Needs Review (Passing: ${normalizedThreshold}%)`}
            </p>
            <p className={styles.scoreTextSub}>
              {passed
                ? 'Outstanding work! You have demonstrated conceptual mastery of this chapter.'
                : 'Review the explanations below and retake the quiz to cement your understanding.'}
            </p>
          </div>
        </div>
      )}

      {/* Persisted Previous Score Badge (if not currently submitted) */}
      {!isSubmitted && persistedRecord && (
        <div
          style={{
            marginBottom: '1.25rem',
            padding: '0.6rem 1rem',
            borderRadius: '8px',
            background: 'rgba(255, 255, 255, 0.04)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            fontSize: '0.85rem',
            color: '#94a3b8',
          }}
        >
          Last Recorded Score:{' '}
          <strong style={{ color: persistedRecord.passed ? '#34d399' : '#f87171' }}>
            {persistedRecord.score}% ({persistedRecord.passed ? 'Passed ✓' : 'Failed'})
          </strong>
        </div>
      )}

      {/* Question List */}
      <div>
        {safeQuestions.map((q, qIndex) => {
          const selectedOption = selectedOptions[q.id];
          const isCorrect = isSubmitted && selectedOption === q.correctIndex;

          return (
            <div key={q.id} className={styles.questionItem}>
              <div className={styles.questionTitle}>
                {qIndex + 1}. {q.question}
              </div>

              <div className={styles.optionsList} role="radiogroup" aria-label={q.question}>
                {q.options.map((opt, optIndex) => {
                  const isOptionSelected = selectedOption === optIndex;
                  let optionClass = styles.optionLabel;

                  if (isSubmitted) {
                    optionClass += ` ${styles.optionDisabled}`;
                    if (optIndex === q.correctIndex) {
                      optionClass += ` ${styles.optionCorrect}`;
                    } else if (isOptionSelected) {
                      optionClass += ` ${styles.optionIncorrect}`;
                    }
                  } else if (isOptionSelected) {
                    optionClass += ` ${styles.optionSelected}`;
                  }

                  return (
                    <label
                      key={optIndex}
                      className={optionClass}
                      onClick={() => handleSelectOption(q.id, optIndex)}
                    >
                      <input
                        type="radio"
                        name={`question-${q.id}`}
                        checked={isOptionSelected}
                        disabled={isSubmitted}
                        onChange={() => handleSelectOption(q.id, optIndex)}
                        className={styles.radioInput}
                        aria-label={opt}
                      />
                      <span>{opt}</span>
                    </label>
                  );
                })}
              </div>

              {/* Immediate pedagogical explanation */}
              {isSubmitted && (
                <div className={styles.explanationBox}>
                  <strong>Explanation: </strong>
                  {q.explanation}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Action Footer */}
      <div className={styles.footerRow}>
        {!isSubmitted ? (
          <>
            <button
              type="button"
              disabled={!isAllAnswered}
              onClick={handleSubmit}
              className={`${styles.actionButton} ${styles.submitButton}`}
            >
              <span>Submit Answers</span>
              <span>→</span>
            </button>
            {!isAllAnswered && (
              <span className={styles.validationNotice}>
                Please answer all {safeQuestions.length} questions ({answeredCount}/{safeQuestions.length} completed)
              </span>
            )}
          </>
        ) : (
          <button
            type="button"
            onClick={handleRetake}
            className={`${styles.actionButton} ${styles.retakeButton}`}
          >
            <span>🔄</span>
            <span>Retake Quiz</span>
          </button>
        )}
      </div>
    </div>
  );
}

export default QuizEngine;
