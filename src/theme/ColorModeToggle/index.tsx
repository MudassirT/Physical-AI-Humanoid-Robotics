import React, {type ReactNode, useCallback} from 'react';
import clsx from 'clsx';
import useIsBrowser from '@docusaurus/useIsBrowser';
import {translate} from '@docusaurus/Translate';
import IconLightMode from '@theme/Icon/LightMode';
import IconDarkMode from '@theme/Icon/DarkMode';
import type {Props} from '@theme/ColorModeToggle';
import type {ColorMode} from '@docusaurus/theme-common';

import styles from './styles.module.css';

function getColorModeLabel(colorMode: ColorMode | null): string {
  return colorMode === 'dark'
    ? translate({
        message: 'dark mode',
        id: 'theme.colorToggle.ariaLabel.mode.dark',
        description: 'The name for the dark color mode',
      })
    : translate({
        message: 'light mode',
        id: 'theme.colorToggle.ariaLabel.mode.light',
        description: 'The name for the light color mode',
      });
}

function getColorModeAriaLabel(colorMode: ColorMode | null) {
  return translate(
    {
      message: 'Switch between dark and light mode (currently {mode})',
      id: 'theme.colorToggle.ariaLabel',
      description: 'The ARIA label for the color mode toggle',
    },
    {
      mode: getColorModeLabel(colorMode),
    },
  );
}

function CurrentColorModeIcon(): ReactNode {
  return (
    <>
      <IconLightMode
        aria-hidden
        className={clsx(styles.toggleIcon, styles.lightToggleIcon)}
      />
      <IconDarkMode
        aria-hidden
        className={clsx(styles.toggleIcon, styles.darkToggleIcon)}
      />
    </>
  );
}

function ColorModeToggle({
  className,
  buttonClassName,
  value,
  onChange,
}: Props): ReactNode {
  const isBrowser = useIsBrowser();

  /**
   * Deterministic synchronous theme toggle.
   * Directly queries the live DOM attribute 'data-theme' to prevent stale React closures
   * when the user clicks the toggle continuously or in rapid succession.
   */
  const handleToggle = useCallback(() => {
    if (typeof document === 'undefined') {
      return;
    }

    // Read the true current DOM state
    const currentTheme =
      document.documentElement.getAttribute('data-theme') || value || 'dark';
    const nextMode: ColorMode = currentTheme === 'dark' ? 'light' : 'dark';

    // Synchronously mutate DOM attributes immediately
    document.documentElement.setAttribute('data-theme', nextMode);
    document.documentElement.setAttribute('data-theme-choice', nextMode);

    try {
      localStorage.setItem('theme', nextMode);
    } catch {
      // Storage access may be blocked in some iframe/sandboxed environments
    }

    // Synchronize React state
    onChange(nextMode);
  }, [value, onChange]);

  return (
    <div className={clsx(styles.toggle, className)}>
      <button
        className={clsx(
          'clean-btn',
          styles.toggleButton,
          !isBrowser && styles.toggleButtonDisabled,
          buttonClassName,
        )}
        type="button"
        onClick={handleToggle}
        disabled={!isBrowser}
        title={getColorModeLabel(value)}
        aria-label={getColorModeAriaLabel(value)}
      >
        <CurrentColorModeIcon />
      </button>
    </div>
  );
}

export default React.memo(ColorModeToggle);
